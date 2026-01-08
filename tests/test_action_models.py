import pytest
from action_models import AndroidAction, TapAction, TypeAction, NavigationAction, ControlAction

def test_tap_action_valid():
    action = TapAction(coordinates=[100, 200], reason="tap button")
    assert action.action == "tap"
    assert action.coordinates == [100, 200]
    assert action.reason == "tap button"

def test_tap_action_invalid_coordinates():
    with pytest.raises(ValueError):
        TapAction(coordinates=[100], reason="invalid")

def test_type_action_valid():
    action = TypeAction(text="Hello", reason="enter text")
    assert action.action == "type"
    assert action.text == "Hello"

def test_navigation_action_home():
    action = NavigationAction(action="home", reason="go home")
    assert action.action == "home"

def test_control_action_done():
    action = ControlAction(action="done", reason="complete")
    assert action.action == "done"
