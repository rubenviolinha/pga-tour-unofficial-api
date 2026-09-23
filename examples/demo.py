"""A few direct calls using pga_api.py. Run from this directory."""

from pathlib import Path

from pga_api import PgaApi


ROOT = Path(__file__).resolve().parents[1]
api = PgaApi()

# REST: season schedule
schedule = api.rest("schedule/R/2026")
print("Schedule events:", len(schedule["tournaments"]))

# REST: full player directory
players = api.rest("player/list/R")
print("Player response keys:", list(players))

# GraphQL: any PGA TOUR stat
stats = api.graphql_file(
    ROOT / "graphql" / "StatDetails.graphql",
    {
        "tourCode": "R",
        "statId": "02675",  # Strokes Gained: Total
        "year": 2026,
        "eventQuery": None,
    },
)
print("Stat rows:", len(stats["statDetails"]["rows"]))

# GraphQL: completed event leaderboard
leaderboard_response = api.graphql_file(
    ROOT / "graphql" / "LeaderboardCompressedV3.graphql",
    {"leaderboardCompressedV3Id": "R2026030"},
)
leaderboard = api.decompress(
    leaderboard_response["leaderboardCompressedV3"]["payload"]
)
for row in leaderboard["players"][:5]:
    print(row["scoringData"]["position"], row["player"]["displayName"])
