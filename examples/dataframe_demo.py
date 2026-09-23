"""Quick tour of the normalized pandas interface."""

import pga_tour_api as pga


tournament_id = "R2026030"

leaderboard = pga.pga_leaderboard(tournament_id)
print(leaderboard[["position", "display_name", "total", "round_4"]].head())

schedule = pga.pga_schedule(2026)
print(schedule[["tournament_id", "tournament_name", "status"]].head())

stats = pga.pga_stats(
    ["02675", "02567", "02568", "02564"],
    year=[2025, 2026],
)
print(stats[["stat_id", "year", "rank", "player_name"]].head())

driving_stats = pga.STAT_IDS[
    pga.STAT_IDS["stat_name"].str.contains("Driving", case=False)
]
print(driving_stats.head())
