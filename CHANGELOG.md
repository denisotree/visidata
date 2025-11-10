# Visidata NG Changelog

<!-- //windsurf-scope: RENAME-REPO -->

## 1.02 (2025-11-10)

- Added date type selection palette on `@` and made it robust against non-string palette fields.
- Improved date parsing to handle bracketed timezone annotations (e.g. `Z[UTC]`) and normalize `Z` to `+00:00`.
- Fixed `AttributeError` arising from `.lower()` on `None` in date-type workflows and status reporting.
- Introduced `copyDateMetadata` to preserve date formatting on derived columns.

## 1.01 (2025-11-09)

- Added currency selection palette when typing columns as currency, including top global and regional currencies.
- Preserved currency symbols and formatting when grouping or creating pivot tables.
- Expanded currency metadata APIs to share formatting across derived columns.

## 1.0 (2025-11-09)

- Initial public release of Visidata NG as an independent fork of VisiData.
- Established project naming, README, and contributing guidelines tailored to the fork.
- Reconfirmed GPLv3 licensing obligations, preserving upstream attribution and outlining redistribution expectations.
