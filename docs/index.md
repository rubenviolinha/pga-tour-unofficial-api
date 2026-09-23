# PGA TOUR Unofficial API

A self-contained Python client and endpoint reference for the public data calls
used by `pgatour.com`.

!!! warning "Unofficial interface"
    PGA TOUR does not document or support these endpoints. Fields, routes, and
    the public browser key may change without notice. This project is not
    affiliated with or endorsed by PGA TOUR.

## What you can retrieve

- Full and compact leaderboards
- Hole-by-hole scorecards and whole-field scoring
- Shot-level play-by-play, coordinates, distances, and radar fields
- Tee times, fields, withdrawals, current form, and course fit
- Season schedules, tournament metadata, weather, and course statistics
- Player profiles, career summaries, results, biographies, and stat profiles
- 400+ statistical rankings and multiple standings systems
- News, video, coverage, and active betting-market data

## Install directly from this repository

```bash
pip install git+https://github.com/rubenviolinha/pga-tour-unofficial-api.git
```

Because the repository is currently private, GitHub authentication is required.

## Quick example

```python
from pga_tour_api import PgaApi

api = PgaApi()
tournament_id = api.current_tournament()

leaderboard = api.leaderboard(tournament_id)
schedule = api.schedule(2026)
players = api.players()
sg_total = api.stats("02675", year=2026)
```

The package has no runtime dependencies. It returns native Python dictionaries
and lists, leaving DataFrame conversion or persistence to the caller.

## Data surfaces

| Surface | Role |
|---|---|
| GraphQL orchestrator | Tournament scoring, stats, standings, weather, content |
| REST data API | Players, schedules, profiles, results, and odds |
| Configuration host | Current tournament IDs and active seasons |
| Server-rendered HTML | Fallback leaderboard and tournament metadata |

Start with [Getting started](getting-started.md), or use the
[raw endpoint catalog](endpoints.md) if you do not need the Python client.
