# Changelog

## 0.3.3 — 2026-09-24

- Add DP World Tour Race to Dubai PGA TOUR eligibility standings (ranking ID 2700).

## 0.3.2 — 2026-09-24

- Add PGA TOUR University rankings and total-points operations with season/week filters.
- Preserve player event histories, source headers and navigation metadata.

## 0.3.0 — 2026-09-24

- Add raw and normalized scorecard statistics, full course/hole rankings, record catalogue and record tables.
- Add searchable record catalogue documentation; preserve source values and selector metadata.
- Bundle four more GraphQL operations; 43 convenience functions (36 DataFrames), 48 raw methods, 106 offline tests.
- Live smoke checks returned 103 scorecard-stat rows, 41 courses, 738 holes, 282 record IDs and 86 rows for record 2-1-11. Dataset sizes are snapshots, not coverage guarantees.
- Warning: upstream record tables may contain anomalous or incomplete entries; values are not independently corrected.

## 0.2.0 — 2026-09-23

- Added 39 `pga_*` convenience functions, 32 of which return normalized pandas DataFrames.
- Made all 467 stat IDs importable through `STAT_IDS`.
- Added multi-stat and multi-season batching.
- Added structured errors, logging, retries, and environment overrides.
- Added 43 offline fixtures and 88 passing tests.
- Added Linux/macOS CI across Python 3.9–3.13.
- Expanded the documentation with complete references, return schemas,
  troubleshooting, development guidance, and version history.

## 0.1.0 — 2026-09-23

- Initial raw client, endpoint catalog, GraphQL documents, validation report,
  sample data, and MkDocs preview.
