"""Load and access guidance YAML files.

This module provides helpers to read guidance content from
``docs/field_hints.yml`` and ``docs/rulebook.yml``. Loaded data is cached
in ``st.session_state['guidance']`` with separate versions for each pack.

The helpers are lightweight and intentionally schema-aware so that YAML
files are the single source of truth for field explanations and rulebook
copy.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import streamlit as st
import yaml

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_field_hints(path: Path | None = None) -> Dict[str, Any]:
    """Load field hints from YAML and cache them in session state."""
    path = path or DOCS_DIR / "field_hints.yml"
    data = _load_yaml(path)
    version = str(data.get("version", ""))
    hints = {k: v for k, v in data.items() if k != "version"}
    st.session_state.setdefault("guidance", {})
    st.session_state["guidance"]["hints"] = hints
    st.session_state["guidance"].setdefault("versions", {})["hints"] = version
    return hints


def load_rulebook(path: Path | None = None) -> Dict[str, Any]:
    """Load rulebook entries from YAML and cache them in session state."""
    path = path or DOCS_DIR / "rulebook.yml"
    data = _load_yaml(path)
    version = str(data.get("version", ""))
    rules = {k: v for k, v in data.items() if k != "version"}
    st.session_state.setdefault("guidance", {})
    st.session_state["guidance"]["rules"] = rules
    st.session_state["guidance"].setdefault("versions", {})["rules"] = version
    return rules


def get_type_hint(type_id: str) -> Dict[str, Any]:
    """Return the hint block for a given income/debt type."""
    return st.session_state.get("guidance", {}).get("hints", {}).get(type_id, {})


def get_field_hint(type_id: str, field: str) -> Dict[str, Any]:
    """Return the hint for a specific field within a type."""
    return get_type_hint(type_id).get(field, {})


def get_rule_text(code: str, program: str | None = None) -> Dict[str, Any]:
    """Return rulebook text for a finding code, optionally filtered by program."""
    rule = st.session_state.get("guidance", {}).get("rules", {}).get(code, {})
    applies = rule.get("applies_to")
    if applies and program and program not in applies and "global" not in applies:
        return {}
    return rule

