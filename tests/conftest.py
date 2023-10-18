"""Fixtures"""


import pytest


@pytest.fixture
def name():
    """Create a testing object"""
    return "someone"


@pytest.fixture
def number():
    """Create a testing object"""
    return 123
