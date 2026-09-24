# Expansion roadmap

Research date: **2026-09-24**. These additions were discovered by inspecting
public PGA TOUR pages and their shipped query documents, then making selected
live requests. The first three priorities are now **implemented in version 0.3.0**:
scorecard statistics, course/hole rankings and all-time records. Remaining
items are research candidates, not implemented features.

## Live-verified additions

| Priority | Addition | Evidence from this investigation | Proposed package support |
|---|---|---|---|
| Delivered | Player tournament performance statistics | `ScorecardStatsV3Compressed` returned and decoded player `59095`'s statistics for event `R2026030`, including strokes gained, ranks, and year-to-date comparisons. | A raw method and a normalized table of player statistics by round and category. |
| 1 | Full course and hole rankings | `CourseStatsDetails` returned 41 courses for `TOUGHEST_COURSE` and 738 holes for `TOUGHEST_HOLES`, using tour `R`, year `2026`, and round `ALL`. Season selectors extended back to 2008. | Full ranking tables with season, round, and ranking-type filters, beyond the existing overview. |
| 1 | All-time records | `AllTimeRecordCategories` returned 282 distinct record IDs across 13 categories. `AllTimeRecordStat` returned 86 rows for record `2-1-11` (lowest 18-hole score). | A separate searchable record catalogue and record-detail function. These IDs are distinct from the 467 season-stat IDs. |
| Delivered | Season-level player comparisons | `PlayerComparison` returned a comparison table for players `59095` and `34046`, tour `R`, year `2026`, category `SCORING`. | Player comparisons by year and category, beyond the existing tournament scorecard comparison. |
| 2 | PGA TOUR University rankings | `UniversityRankings` returned 92 players for season `2027`, plus week/year selectors and player event results. | Ranking and event-result tables with year/week filters. |
| 2 | PGA TOUR University total points | `UniversityTotalPoints` returned 24 players for season `2026`, with season/week navigation. | A separate qualification-points table. |

These are snapshot results, not fixed dataset sizes. One successful request
does not establish coverage for every season, player, tour, or record ID.
In particular, the 282-record catalogue was enumerated, but all 282 record
detail calls were not individually tested.

## Website data confirmed; direct API still to verify

- **DP World Tour eligibility rankings:** the public page contained structured
  `dpWorldTourRankings` data with 21 official players for 2026. Discover and
  validate the direct request before adding a supported client function.

## Query definitions found; usable data still to verify

| Area | Examples of discovered operations | Remaining work |
|---|---|---|
| Playoffs | `PlayoffScorecardV3`, `PlayoffShotDetailsCompressed` | Test completed playoff events and decode the scorecard/shot structures. |
| Team and match play | `TeamStrokePlayLeaderboardCompressed`, `MatchPlayLeaderboardCompressed`, `CupTeamRoster` | Verify suitable event IDs, scoring formats, rosters, and empty-result behavior. |
| Historical odds | `HistoricalOdds`, `HistoricalTournamentsOdds` | Determine supported market values and historical availability. |
| Editorial ranking tables | `GetPowerRankingsTable`, `GetExpertPicksTable` | Verify article paths and structured table responses. |
| Leaderboard statistics/probabilities | `LeaderboardStats` | The default request for completed event `R2026030` returned type `PROBABILITY` with no players. Verify supported types against appropriate events before claiming coverage. |

## Delivery checklist

For each addition:

- [ ] Verify the complete request and relevant filters against live data.
- [ ] Bundle the query document and any required fragments.
- [ ] Add raw access and a normalized function where the response fits a table.
- [ ] Preserve identifiers, season/round context, and response metadata.
- [ ] Add representative fixtures and tests for populated and empty responses.
- [ ] Document parameters, return columns, limitations, and a working example.
- [ ] Update the endpoint manifest, changelog, and counts only after implementation.

## Sources

- [PGA TOUR statistics and records](https://www.pgatour.com/stats)
- [Toughest courses](https://www.pgatour.com/stats/course/toughest-course)
- [Toughest holes](https://www.pgatour.com/stats/course/toughest-holes)
- [PGA TOUR University](https://www.pgatour.com/university)
- [University total points](https://www.pgatour.com/university/total-points)
- [DP World Tour eligibility rankings](https://www.pgatour.com/dp-world-tour-eligibility-rankings)

The query definitions were observed in the site's public frontend bundle
`_app-1177e9b067f9f99b.js` (build `pgatour-prod-2.32.2`). Bundle names may change;
discover the scripts from the current page when repeating the investigation.
