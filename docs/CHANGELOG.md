# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Compact bottom summary drawer with snapshot totals.
- Initial project scaffolding and mandatory metadata files.
- Borrower sidebar cards for name, contact, and credit info with top bar dropdown selection.

### Fixed
- Install pytest in CI workflow to enable test execution.
- Scrollable container layout with bottom bar document checklist.
- Sidebar and bottom bar toggle arrows with dark gray styling.
- Sidebar headers now appear inside their bordered boxes for clearer grouping.
- Replace deprecated `st.experimental_rerun` calls with `st.rerun` for Streamlit 1.27+ compatibility.
- Missing income cards and overflowing disclosure box by restructuring layout with Streamlit columns.
- Prevent type errors in bottom bar when FE/BE targets are provided as strings.
- Blank drawer when adding income or debt cards due to incorrect editor state.
- Sidebar drawer rendered empty because widgets were outside the HTML container; content now uses Streamlit's sidebar.
- Removed sidebar toggle arrow and restored income and debt boards to main layout with a wider persistent sidebar.
- Sidebar editor width now doubles `SIDEBAR_WIDTH` using the updated `section[data-testid='stSidebar']` selector for consistency.

### Changed
- Removed left data-entry column; main grid shows income, debts, and property boxes only.
- Sidebar remains visible for data entry with disclosures and guides.
