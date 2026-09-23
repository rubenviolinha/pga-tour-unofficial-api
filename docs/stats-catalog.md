# Statistics catalog

The package exports `STAT_IDS`, a searchable pandas DataFrame containing 467
discovered stat IDs, names, categories, and subcategories.

```python
import pga_tour_api as pga

print(pga.STAT_IDS.head())

putting = pga.STAT_IDS[pga.STAT_IDS["category"] == "Putting"]
driving = pga.STAT_IDS[
    pga.STAT_IDS["stat_name"].str.contains("Driving", case=False)
]
```

Stat IDs are strings. Preserve leading zeroes such as `"02675"`.

## Common IDs

| ID | Statistic |
|---|---|
| `02675` | SG: Total |
| `02674` | SG: Tee-to-Green |
| `02567` | SG: Off-the-Tee |
| `02568` | SG: Approach the Green |
| `02569` | SG: Around-the-Green |
| `02564` | SG: Putting |
| `101` | Driving Distance |
| `102` | Driving Accuracy Percentage |
| `103` | Greens in Regulation Percentage |
| `120` | Scoring Average (Adjusted) |
| `130` | Scrambling |

The complete snapshot is also available as
[`data/stat_ids.csv`](data/stat_ids.csv). To discover changes directly from the
site, call `pga.pga_stats` for known IDs or use the raw `StatOverview` operation.
