"""Tests for rlway_cpagent."""


import pytest

from rlway_cpagent.utils.utils import greet


def test_greet_with_str(name):
    """make sure greet function works well with strings
    """
    result = greet(name)
    expected_msg = "Hello someone!"
    assert result == expected_msg


def test_greet_with_int(number):
    """make sure greet function errors when used with an integer
    """
    with pytest.raises(TypeError):
        greet(number)
