# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Sticky summary band beneath top bar with snapshot totals.
- Dashboard metrics surface Total Income, PITIA, FE DTI, and BE DTI.
- Initial project scaffolding and mandatory metadata files.
- Borrower sidebar cards for name, contact, and credit info with top bar dropdown selection.
- Income and debt cards now display borrower, type, employer/title, and monthly totals.
- Income card creation now allows selecting the income type instead of defaulting to W-2 only.
- Users can duplicate and remove income and debt cards.
- YAML-driven guidance spec with loaders, rulebook, and panel scaffolding.
- Borrowers can be removed from the sidebar, clearing their related income and debt cards.

### Changed
- Income and debt cards open the editor when clicked; duplicate and remove actions use icon buttons.
- Income and debt cards now show a single bordered box with inline duplicate and remove buttons.

### Fixed
- Install pytest in CI workflow to enable test execution.
- Scrollable container layout with bottom bar document checklist.
- Sidebar and bottom bar toggle arrows with dark gray styling.
- Sidebar headers now appear inside their bordered boxes for clearer grouping.
- Replace remaining deprecated `st.experimental_rerun` call with `st.rerun` for Streamlit 1.27+ compatibility.
- Missing income cards and overflowing disclosure box by restructuring layout with Streamlit columns.
- Prevent type errors in bottom bar when FE/BE targets are provided as strings.
- Blank drawer when adding income or debt cards due to incorrect editor state.
- Sidebar drawer rendered empty because widgets were outside the HTML container; content now uses Streamlit's sidebar.
- Removed sidebar toggle arrow and restored income and debt boards to main layout with a wider persistent sidebar.
- Sidebar editor width now doubles `SIDEBAR_WIDTH` using the updated `section[data-testid='stSidebar']` selector for consistency.
- Property info panel now renders in a third column to the right of debts.
- Sidebar toggle now hides the drawer completely.

- Removed left data-entry column; main grid shows income, debts, and property boxes only.
- Sidebar remains visible for data entry with disclosures and guides.
- Replaced bottom summary drawer with top summary band.
- Dashboard DTI metrics show "—" when income is missing instead of extreme percentages.
- Add missing `__init__.py` for `ui` package to resolve `KeyError` on import.
