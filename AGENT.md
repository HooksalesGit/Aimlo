# AGENT.md — AMALO Engineering Agent Playbook
**Date:** 2025-08-22

This file defines how the autonomous agent (and human contributors) plan, implement, test, and release changes to the **AMALO** mortgage app. It encodes the standards required for reliability, clarity, and MLO-first usability.

---

## 1) Mission & Purpose
AMALO is the **primary qualification tool** for a Florida Mortgage Loan Originator (MLO). Every change **must** make the MLO’s life **faster, clearer, more reliable**.

**Product goals**
- **Speed:** Enter borrower data once; instantly see incomes, PITIA, FE/BE DTI, LTV, and max qualifiers.
- **Correctness:** Mirror common UW logic (W‑2, Sch C, K‑1, 1120, rentals; program-aware MI/MIP/funding fees; student-loan policies).
- **Guardrails:** Warnings with concrete remedies, export gating for critical issues, “Where to find it” pointers for each field.
- **Explainability:** Every field has a short definition and “where to find it” source, fed from a single YAML file.

---

## 2) Non‑Negotiable Principles
1) **Explain fields**: All user-facing field help lives in `docs/field_hints.yml`. The app’s **Guidance Center** reads it at runtime. No new field without an entry here.
2) **No regressions**: Every PR that changes logic adds tests (unit + at least one integration). **Golden scenarios** must remain green.
3) **Visible version**: `core/version.py` defines `__version__ = "MAJOR.MINOR.PATCH"`. The top bar shows `AMALO — v{__version__}`.
4) **Change is tracked**: `docs/CHANGELOG.md` (Keep a Changelog). Each PR updates the **Unreleased** section.
5) **MLO-first UX**: Card-based **forms** (not raw tables) for input; plain language labels; warnings explain actions; minimal clicks to results.
6) **Design consistency**: Use `ui/theme.py` tokens (spacing, radii, colors, shadows, typography) in all new UI.

---

## 3) Repository Structure (authoritative)
```
app.py
/core/
  calculators.py
  rules.py
  presets.py
  models.py
  scenarios.py
  version.py
/ui/
  theme.py
  topbar.py
  layout.py
  sidebar_editor.py
  bottombar.py
  tabs_dashboard.py
/export/
  pdf_export.py
/tests/
  unit/
  integration/
  golden/            # canonical scenarios (inputs + expected outputs)
/docs/
  PRD.md
  RULES.md
  SCENARIOS.md
  CHANGELOG.md
  field_hints.yml
  CONTRIBUTING.md
.github/
  workflows/ci.yml
  PULL_REQUEST_TEMPLATE.md
```

---

## 4) Branch & PR Workflow
- Branch names: `feat/<name>`, `fix/<name>`, `chore/<name>`.
- **Conventional Commits** in messages: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
- Keep PRs small (<500 LOC when feasible), **one change per PR**.
- Attach **screens/GIFs** for any UX change.

---

## 5) Definition of Done (DoD)
- Code implemented; smallest surface area; follows existing structure.
- **Tests added/updated** (unit + at least one integration path). Golden scenarios updated only if expected outputs intentionally change.
- `docs/CHANGELOG.md` updated (under **Unreleased**).
- `docs/field_hints.yml` updated for any new/changed field.
- `core/version.py` bumped (SemVer: patch=fix, minor=feature, major=breaking).
- Top bar displays the new version automatically.
- App launches; no critical rules broken; CI green.

---

## 6) Testing Policy (with Coverage Gate)
- **Unit**: amortization & inverse, MI/MIP/funding fees, student-loan policy payments, rules, helpers.
- **Integration**: end-to-end compute (income → PITIA → DTI).
- **Golden**: maintain ≥10 canonical scenarios in `tests/golden/` with expected outputs; failures **block** merges.
- **UX smoke**: existence of key widgets/labels to prevent accidental removal.
- **Coverage gate**: **≥85%** combined line coverage over `core/` and `ui/` (measured in CI). This prevents silent math regressions.

---

## 7) Changelog & Versioning
- **Keep a Changelog** in `docs/CHANGELOG.md` with sections: **Added / Changed / Fixed / Deprecated / Removed / Security**.
- **SemVer**: `MAJOR.MINOR.PATCH` in `core/version.py`. The top bar renders `vX.Y.Z`.
- Create annotated tags on release: `vX.Y.Z`. Release notes sourced from the changelog.

---

## 8) UX & Explainability Rules
- Input = **forms** inside cards; no raw editable tables for data entry.
- Each field shows label + sublabel pulled from `docs/field_hints.yml`.
- **Guidance Center** side panel provides a 3-way toggle: **Guides**, **Warnings**, **Where to find**.
- Warnings include a **“Fix this”** deep link that focuses the exact card/field.
- Optional bottom bar: **Total Income / PITIA / FE / BE** with PASS/CHECK at a glance.

---

## 9) Mortgage Guardrails (must keep)
- Student loan policies (Conventional/FHA/VA/USDA): impute when not fully amortizing or undocumented.
- **1120** income counts only with **100% ownership**.
- **K‑1** requires **verified distributions** or **documented business liquidity**.
- **Schedule C** two-year averaging; decline warnings if YOY down materially.
- **Rentals**: mutually exclusive methods (Schedule E vs 75% gross; subject add-on uses 75% market rent − PITIA).
- **Support income**: require ≥3-year continuance.
- DTI thresholds from program presets; high LTV banners; property sanity tips.

---

## 10) Agent Operating Rules (Codex)
When a new request arrives, the agent must **always**:
1) **Clarify only critical ambiguity**; otherwise proceed with reasonable defaults.
2) **Plan** briefly in the PR description: tasks → code → tests → docs → version.
3) **Implement** the smallest viable change; keep modules cohesive.
4) **Sync explanations**: update `docs/field_hints.yml` for every new/changed field.
5) **Test**: add/adjust unit & integration; update/add a golden scenario only when intended output changes are justified.
6) **Changelog**: append under **Unreleased**.
7) **Version**: bump `core/version.py` appropriately.
8) **PR**: include UX screenshots/GIFs; reference affected warnings/guardrails; ensure CI passes.

**Acceptance checklist (every PR)**
- [ ] Tests added/updated (unit + at least one integration)
- [ ] Golden scenarios pass (or updated intentionally)
- [ ] `docs/CHANGELOG.md` updated (Unreleased)
- [ ] `docs/field_hints.yml` updated (new/changed fields)
- [ ] Version bumped in `core/version.py` and visible in top bar
- [ ] UX screenshots/GIFs attached
- [ ] CI green; coverage ≥85%

---

## 11) Built‑in “Make MLO Life Easier” Features (Roadmap & Defaults)
- **Try sample data** button to populate a complete scenario for demos/QA.
- **Scenario Diff Drawer** in Dashboard: “What changed since vX.Y.Z?” (diff of session JSON inputs/outputs).
- **Explain this warning** link jumps to the field and shows a short “why this matters” blurb.
- **Single-source fee tables** in `core/presets.py` with comments linking to investor handbooks used internally.
- Property snapshot click opens sidebar editor, including Florida defaults and MI/MIP tables.

---

## 12) CI Gates (GitHub Actions)
CI must block merges unless all of the following are true:
- Unit + integration tests pass, **coverage ≥85%**.
- Golden scenarios pass.
- `docs/CHANGELOG.md` contains an **Unreleased** entry for the PR.
- `docs/field_hints.yml` is present and non-empty when fields are changed.
- `core/version.py` exists and has a SemVer string.

---

## 13) Quickstart for Agents
1) Create branch: `feat/<name>` or `fix/<name>`.
2) Implement code and **update `docs/field_hints.yml`** for any new/changed fields.
3) Add tests (unit + integration) and adjust golden scenarios only if outputs intentionally change.
4) Update `docs/CHANGELOG.md` under **Unreleased** (Added/Changed/Fixed…).
5) Bump version in `core/version.py`.
6) Open PR with screenshots; ensure CI passes; request review.

---

## 14) Security & Privacy
- Local-only processing; no automatic network calls for PII.
- Only user-initiated exports; no auto-persistence of borrower data.

---

## 15) Appendices

### A) Required Files (presence enforced by CI)
- `core/version.py` — single source of truth for version.
- `docs/CHANGELOG.md` — Keep a Changelog.
- `docs/field_hints.yml` — single source for field help.
- `tests/` — unit, integration, golden.

### B) SemVer Guidance
- **PATCH**: bug fix, no logic changes that alter outputs.
- **MINOR**: new feature or UI/UX improvement that does not break API; may alter outputs intentionally (update golden as needed).
- **MAJOR**: breaking change or large recalculation policy change.
