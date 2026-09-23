# PGA TOUR Unofficial API

A self-contained Python client and endpoint reference for the public browser
data calls used by `pgatour.com`. Access leaderboards, player stats, scorecards,
shot tracking, tee times, standings, odds, schedules, news, and video.

!!! warning "Unofficial interface"
    PGA TOUR does not document or support these endpoints. Fields, routes, and
    the public browser key may change without notice. This project is not
    affiliated with or endorsed by PGA TOUR.

Two interfaces are included: normalized `pga_*` functions returning pandas
DataFrames, and `PgaApi` for callers who prefer raw dictionaries and lists.

## Installation

```bash
pip install git+https://github.com/rubenviolinha/pga-tour-unofficial-api.git
```

## Quick Start

```python
import pga_tour_api as pga

# This week's tournament + leaderboard
tid = pga.pga_current_tournament()
pga.pga_leaderboard(tid)

# Strokes Gained: Total rankings
pga.pga_stats("02675")

# Full player directory (2,700+ players)
pga.pga_players()

# Hole-by-hole scorecard
pga.pga_scorecard(tid, "34046")

# Shot-level tracking with coordinates
pga.pga_shot_details(tid, "34046", round=1)

# Full season schedule
pga.pga_schedule(2026)
```

## Functions Overview

### Live Tournament Data

| Function | Description |
|---|---|
| `pga_current_tournament()` | This week's tournament ID |
| `pga_leaderboard()` | Full leaderboard with scores, positions, and round-by-round results |
| `pga_current_leaders()` | Quick top-15 snapshot for in-progress tournaments |
| `pga_field()` | Tournament field with OWGR and withdrawn flags |
| `pga_field_stats()` | Current-form or course-fit stats for the field |
| `pga_leaderboard_holes()` | Hole-by-hole scores for the whole field |
| `pga_tee_times()` | Tee time groupings with start tees and player assignments |
| `pga_scorecard()` | Hole-by-hole scorecard with par, score, yardage, and status |
| `pga_shot_details()` | Shot-by-shot tracking data with coordinates and play-by-play |
| `pga_odds()` | Betting odds to win for the tournament field |
| `pga_odds_markets()` | Available betting-market catalog |
| `pga_player_odds()` | FanDuel markets for one player |
| `pga_coverage()` | Broadcast and streaming schedule |
| `pga_weather()` | Hourly and daily forecast |
| `pga_course_stats()` | Per-hole scoring averages for the host course |

### Statistics & Standings

| Function | Description |
|---|---|
| `pga_stats()` | Any of 400+ stats with full player rankings (2004-2026) |
| `pga_fedex_cup()` | FedExCup standings with projected and official rankings |
| `pga_signature_standings()` | Signature Event / Aon standings |
| `pga_priority_rankings()` | Exemption / priority ranking categories |
| `pga_scorecard_comparison()` | Head-to-head stat comparison between players |
| `pga_course_stats_overview()` | Season course-stats hub |

### Players & Tournaments

| Function | Description |
|---|---|
| `pga_players()` | Full player directory (2,700+ players) |
| `pga_tournaments()` | Tournament metadata including location, courses, weather |
| `pga_schedule()` | Season schedule with dates, purse, course, champion |
| `pga_tournament_overview()` | Overview tiles, defending champion, past champions |
| `pga_tournament_past_results()` | Historical finishes for an event |

### Player Profiles

| Function | Description |
|---|---|
| `pga_player_profile()` | Overview with career highlights, wins, earnings, world rank, bio |
| `pga_player_career()` | Career achievements: starts, cuts, wins, finish distribution |
| `pga_player_results()` | Tournament-by-tournament results with round scores and earnings |
| `pga_player_stats()` | Full stat profile (131 stats with ranks) in a single call |
| `pga_player_bio()` | Biographical text and amateur highlights |
| `pga_player_tournament_status()` | Live tournament status if currently playing |

### Content

| Function | Description |
|---|---|
| `pga_news()` | News articles with filtering and pagination |
| `pga_news_franchises()` | Available news categories |
| `pga_videos()` | Player video highlights |
| `pga_tourcast_videos()` | Shot-by-shot video clips |
| `pga_content()` | Generic CMS content fragment |
| `pga_odds_interactivity()` | Odds widget configuration |
| `pga_speed_rounds()` | Speed-rounds video index |

### Data

| Variable | Description |
|---|---|
| `STAT_IDS` | pandas DataFrame of 400+ stat IDs with names and categories |

## Tour Codes

| Code | Tour |
|---|---|
| `"R"` | PGA Tour |
| `"S"` | PGA Tour Champions |
| `"H"` | Korn Ferry Tour |
| `"Y"` | PGA Tour Americas |

## Raw response client

```python
from pga_tour_api import PgaApi

api = PgaApi()
raw_leaderboard = api.leaderboard(api.current_tournament())
```

See the [Raw client reference](python-client.md) for every object-oriented
method, or the [raw endpoint catalog](endpoints.md) for direct HTTP use.
