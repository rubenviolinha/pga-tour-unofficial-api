# Responsible use

This project documents an internal website interface, not a supported public
developer API.

## Practical rules

- Cache completed tournaments and historical statistics.
- Avoid repeatedly polling fields that cannot change.
- Use a descriptive User-Agent.
- Keep the default one-second request interval unless there is a clear need to
  change it.
- Back off on `429` and transient server errors.
- Respect PGA TOUR's robots policy, terms, and data licensing.
- Do not bypass login requirements, paywalls, access controls, or geographic
  restrictions.
- Do not treat an empty live-only result as an error outside the event window.

## Stability

The public frontend key, GraphQL schema, compressed payload format, and endpoint
names can change without notice. `PGA_API_KEY` can override a rotated key without
requiring a package update.

## Attribution

The query inventory was cross-checked against the MIT-licensed pgatourPY
project. Query documents derived from that work retain its license notice in
`LICENSES/pgatourPY-MIT.txt`.
