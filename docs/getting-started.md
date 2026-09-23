# Getting started

## Installation

Install the client directly from the private repository:

```bash
pip install git+https://github.com/rubenviolinha/pga-tour-unofficial-api.git
```

For local development:

```bash
git clone https://github.com/rubenviolinha/pga-tour-unofficial-api.git
cd pga-tour-unofficial-api
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Authentication model

The website sends a public frontend key with GraphQL requests. The current
browser key is bundled for convenience, and you can replace it if PGA TOUR
rotates it:

```bash
export PGA_API_KEY="new-public-browser-key"
```

This is not a PGA TOUR developer credential and provides no supported service
guarantee.

## Find the current tournament

```python
from pga_tour_api import PgaApi

api = PgaApi()
tournament_id = api.current_tournament("R")
print(tournament_id)
```

Tour codes:

| Code | Tour |
|---|---|
| `R` | PGA TOUR |
| `S` | PGA TOUR Champions |
| `H` | Korn Ferry Tour |
| `Y` | PGA TOUR Americas |

## Leaderboard

```python
leaderboard = api.leaderboard(tournament_id)

for row in leaderboard.get("players", [])[:10]:
    player = row["player"]
    scoring = row["scoringData"]
    print(scoring["position"], player["displayName"], scoring["total"])
```

Compressed response handling is automatic.

## Schedule and players

```python
schedule = api.schedule(2026, "R")
for event in schedule["tournaments"]:
    print(event["tournamentId"], event["name"], event["displayDate"])

directory = api.players("R")
print(len(directory["players"]))
```

## Player deep dive

```python
player_id = "59095"

profile = api.player_profile(player_id)
career = api.player_career(player_id)
results = api.player_results(player_id, season=2026)
stats = api.player_stats(player_id)
bio = api.player_bio(player_id)
```

## Scorecards and shots

```python
scorecard = api.scorecard("R2026030", "59095")
shots = api.shot_details("R2026030", "59095", round=4)
```

Shot availability varies. Not every tournament has TOURCAST coordinates or
radar measurements for every shot.

## Statistics

Stat IDs are strings and may contain important leading zeroes:

```python
sg_total = api.stats("02675", year=2026)
driving_distance = api.stats("101", year=2026)
all_stats = api.stat_overview(year=2026)
```

The repository includes [`data/stat_ids.csv`](data/stat_ids.csv) with the
full discovered list.

## Raw operations

Every bundled GraphQL document can be called directly:

```python
data = api.graphql(
    "Weather",
    {"tournamentId": "R2026030"},
)
print(data["weather"])
```

For routes and complete variable signatures, see [Raw endpoints](endpoints.md).
