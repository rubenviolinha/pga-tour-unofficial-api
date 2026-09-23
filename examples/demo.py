"""A few calls using the repository's native package."""

from pga_tour_api import PgaApi


api = PgaApi()

# REST: season schedule
schedule = api.rest("schedule/R/2026")
print("Schedule events:", len(schedule["tournaments"]))

# REST: full player directory
players = api.rest("player/list/R")
print("Player response keys:", list(players))

# GraphQL: any PGA TOUR stat
stats = api.stats("02675", year=2026)  # Strokes Gained: Total
print("Stat rows:", len(stats["rows"]))

# GraphQL: completed event leaderboard
leaderboard = api.leaderboard("R2026030")
for row in leaderboard["players"][:5]:
    print(row["scoringData"]["position"], row["player"]["displayName"])
