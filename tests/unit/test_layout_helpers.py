from ui.layout_helpers import build_sidebar_css, SIDEBAR_WIDTH

def test_build_sidebar_css_width_and_visibility():
    css_visible = build_sidebar_css('#000', '#fff', True, SIDEBAR_WIDTH)
    assert f"width:{SIDEBAR_WIDTH}px" in css_visible
    css_hidden = build_sidebar_css('#000', '#fff', False, SIDEBAR_WIDTH)
    assert 'display:none' in css_hidden
