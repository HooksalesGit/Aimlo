import importlib


def test_ui_utils_importable():
    module = importlib.import_module("ui.utils")
    assert hasattr(module, "borrower_name")
