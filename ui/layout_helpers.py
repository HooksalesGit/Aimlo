"""Helper functions for layout styling."""
from __future__ import annotations

# Default width for the sidebar editor drawer. The drawer will clamp to this
# value on wide screens and use 90% of the viewport width on narrow devices.
SIDEBAR_WIDTH = 640


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
.fixed-sidebar{{position:fixed;top:60px;bottom:0;left:0;width:{width}px;background:{panel_bg};color:{panel_text};display:flex;flex-direction:column;border-right:1px solid #ccc;}}
.fixed-sidebar .data{{flex:1;overflow-y:auto;padding:8px;}}
.fixed-sidebar .disc{{border-top:1px solid #ccc;padding:8px;max-height:180px;overflow-y:auto;}}
.main-area{{margin-left:{width}px;padding:0 16px;}}
.sidebar-toggle{{position:fixed;top:70px;left:{width}px;z-index:1000;}}
.sidebar-toggle button{{background:{panel_bg};color:{panel_text};border:none;}}
.scroll-income,.scroll-debt,.scroll-prop{{max-height:400px;overflow-y:auto;border:1px solid #ccc;padding:8px;}}
</style>
"""
    if not visible:
        base += f"""
<style>
.fixed-sidebar{{display:none;}}
.main-area{{margin-left:0;}}
.sidebar-toggle{{left:0;}}
</style>
"""
    return base
