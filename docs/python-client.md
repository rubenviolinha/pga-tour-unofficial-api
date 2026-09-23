# Raw client

`PgaApi` is the lower-level, object-oriented interface. Its convenience methods
decode compressed responses but otherwise preserve upstream field names and
response structures. Use it when you need the original nested JSON rather than
normalized pandas DataFrames.

::: pga_tour_api.PgaApi

::: pga_tour_api.PgaApiError
