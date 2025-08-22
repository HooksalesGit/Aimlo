"""Helper functions for layout styling."""
from __future__ import annotations

SIDEBAR_WIDTH = 260


def build_sidebar_css(panel_bg: str, panel_text: str, visible: bool, width: int = SIDEBAR_WIDTH) -> str:
    """Return CSS for the fixed sidebar and main area.

    Parameters
    ----------
    panel_bg: str
        Background color for sidebar panels.
    panel_text: str
        Text color for sidebar panels.
    visible: bool
        Whether the sidebar should be visible.
    width: int
        Fixed width of the sidebar in pixels.
    """
    base = f"""
<style>
.fixed-sidebar{{position:fixed;top:60px;bottom:0;left:0;width:{width}px;background:{panel_bg};color:{panel_text};display:flex;flex-direction:column;border-right:1px solid #ccc;z-index:100;}}
.fixed-sidebar .data{{flex:1;overflow-y:auto;padding:8px;}}
.fixed-sidebar .disc{{border-top:1px solid #ccc;padding:8px;max-height:180px;overflow-y:auto;}}
.block-container{{margin-left:{width}px;padding-left:16px;padding-right:16px;}}
.sidebar-toggle{{position:fixed;top:70px;left:{width}px;z-index:1000;}}
.sidebar-toggle button{{background:{panel_bg};color:{panel_text};border:none;}}
.scroll-income,.scroll-debt,.scroll-prop{{max-height:400px;overflow-y:auto;border:1px solid #ccc;padding:8px;}}
#bottombar_show button{{background:{panel_bg};color:{panel_text};border:none;}}
#bottombar_show{{position:fixed;bottom:0;right:10px;z-index:1000;}}
</style>
"""
    if not visible:
        base += f"""
<style>
.fixed-sidebar{{display:none;}}
.block-container{{margin-left:0;}}
.sidebar-toggle{{left:0;}}
</style>
"""
    return base
