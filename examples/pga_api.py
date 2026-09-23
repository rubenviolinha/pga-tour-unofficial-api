"""Minimal standard-library client for PGA TOUR's browser-facing data services.

This is an unofficial client. The endpoints and public frontend key can change
without notice. Set PGA_API_KEY to override the bundled browser key.
"""

from __future__ import annotations

import base64
import gzip
import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


GRAPHQL_URL = "https://orchestrator.pgatour.com/graphql"
REST_URL = "https://data-api.pgatour.com"
CONFIG_URL = "https://orchestrator-config.pgatour.com"

# Public key shipped to pgatour.com browsers as of 2026-09-23. It is not a
# user credential, but it may rotate. Prefer the PGA_API_KEY environment var.
DEFAULT_BROWSER_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"


class PgaApiError(RuntimeError):
    pass


class PgaApi:
    def __init__(self, api_key: str | None = None, min_interval: float = 1.0):
        self.api_key = api_key or os.environ.get("PGA_API_KEY") or DEFAULT_BROWSER_KEY
        self.min_interval = min_interval
        self._last_request = 0.0

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://www.pgatour.com",
            "Referer": "https://www.pgatour.com/",
            "User-Agent": "pga-unofficial-api-reference/0.1",
            "x-api-key": self.api_key,
            "x-pgat-platform": "web",
        }

    def _request(self, url: str, body: dict[str, Any] | None = None) -> Any:
        delay = self.min_interval - (time.monotonic() - self._last_request)
        if delay > 0:
            time.sleep(delay)

        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(
            url,
            data=data,
            headers=self._headers(),
            method="POST" if body is not None else "GET",
        )

        for attempt in range(3):
            try:
                self._last_request = time.monotonic()
                with urllib.request.urlopen(request, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code not in {408, 429, 500, 502, 503, 504} or attempt == 2:
                    detail = exc.read(300).decode("utf-8", "replace")
                    raise PgaApiError(f"HTTP {exc.code}: {detail}") from exc
            except urllib.error.URLError as exc:
                if attempt == 2:
                    raise PgaApiError(str(exc)) from exc
            time.sleep((2**attempt) + random.random() / 4)

        raise PgaApiError("request failed after retries")

    def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        first_line = next(line for line in query.splitlines() if line.strip())
        operation_name = first_line.split("(", 1)[0].split()[-1]
        response = self._request(
            GRAPHQL_URL,
            {"operationName": operation_name, "query": query, "variables": variables},
        )
        if response.get("errors"):
            messages = "; ".join(item.get("message", "") for item in response["errors"])
            raise PgaApiError(messages)
        return response.get("data", {})

    def graphql_file(self, path: str | Path, variables: dict[str, Any]) -> dict[str, Any]:
        return self.graphql(Path(path).read_text(), variables)

    def rest(self, path: str) -> Any:
        return self._request(f"{REST_URL}/{path.lstrip('/')}")

    def config(self, path: str = "web-config") -> Any:
        return self._request(f"{CONFIG_URL}/{path.lstrip('/')}")

    @staticmethod
    def decompress(payload: str) -> Any:
        """Decode the base64(gzip(JSON)) payload returned by *Compressed queries."""
        return json.loads(gzip.decompress(base64.b64decode(payload)))


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    api = PgaApi()

    config = api.config()
    tournament_id = config["defaultTournaments"]["R"][0]["leaderboardId"]
    print("Current PGA TOUR tournament:", tournament_id)

    data = api.graphql_file(
        root / "graphql" / "LeaderboardCompressedV3.graphql",
        {"leaderboardCompressedV3Id": tournament_id},
    )
    leaderboard = PgaApi.decompress(data["leaderboardCompressedV3"]["payload"])
    print("Leaderboard players:", len(leaderboard.get("players", [])))
