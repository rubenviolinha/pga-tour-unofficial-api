# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Publish the documentation site when repository visibility permits.
- Add type-safe response models as an optional interface.

## [0.2.0] - 2026-09-23

### Added

- Normalized pandas DataFrame interface with 39 `pga_*` functions.
- Importable `STAT_IDS` catalog with 467 discovered statistics.
- Multi-stat and multi-season batching for `pga_stats`.
- Request logging, bounded retries, public-key override, and transport errors.
- 43 offline API fixtures and 88 passing tests.
- Linux/macOS CI across Python 3.9–3.13.
- Expanded documentation, troubleshooting, schemas, and complete API reference.

### Changed

- Moved the original object-oriented raw client to `pga_tour_api.raw` while
  retaining `from pga_tour_api import PgaApi` compatibility.

## [0.1.0] - 2026-09-23

### Added

- Initial raw client, endpoint catalog, GraphQL documents, validation report,
  and local MkDocs site.
