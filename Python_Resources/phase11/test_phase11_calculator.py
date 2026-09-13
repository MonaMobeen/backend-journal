""" HOW I TRYNA RUN THIS FILE:
1. Install pytest first (one time):
   pip install pytest --break-system-packages

2. Run all tests in this file from the terminal:
   pytest test_phase11_calculator.py -v

pytest automatically finds any file starting with "test_" and any
function starting with "test_" inside it - that's "test discovery".
"""

import pytest
from unittest.mock import patch

from phase11_calculator import add, divide, is_even, ShoppingCart


# ---------- Basic Unit Tests ----------
# A unit test checks ONE small piece of behavior in isolation.
def test_add():
    assert add(2, 3) == 5


def test_add_with_negative_numbers():
    assert add(-2, -3) == -5


# ---------- Testing Expected Failures ----------
def test_divide_by_zero_raises_error():
    """pytest.raises checks that a specific exception IS raised - this
    test PASSES only if the ValueError actually happens."""
    with pytest.raises(ValueError):
        divide(10, 0)


def test_divide_normal_case():
    assert divide(10, 2) == 5


# ---------- Parameterized Tests ----------
# Instead of writing the same test multiple times with different values,
# @pytest.mark.parametrize runs the same test function once per data set.
@pytest.mark.parametrize(
    "number, expected",
    [
        (2, True),
        (3, False),
        (0, True),
        (-4, True),
        (-7, False),
    ],
)
def test_is_even(number, expected):
    assert is_even(number) == expected


# ---------- Fixtures ----------
# A fixture provides a reusable piece of setup that multiple tests can share,
# instead of repeating the same setup code in every test function.
@pytest.fixture
def empty_cart():
    """Provides a fresh, empty ShoppingCart for any test that needs one."""
    return ShoppingCart()


def test_cart_starts_empty(empty_cart):
    assert empty_cart.total() == 0


def test_cart_add_item(empty_cart):
    empty_cart.add_item("Book", 15.0)
    assert empty_cart.total() == 15.0


def test_cart_add_multiple_items(empty_cart):
    empty_cart.add_item("Book", 15.0)
    empty_cart.add_item("Pen", 2.5)
    assert empty_cart.total() == 17.5


def test_cart_rejects_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Broken Item", -5)


# ---------- Mocking Basics ----------
# Mocking replaces a real function/dependency with a fake, controllable
# version - useful when the real thing is slow, costly, or unpredictable
# (e.g. an external API call, sending a real email, or today's date).
def get_shipping_fee_from_api():
    """
    Imagine this makes a real network call to a shipping provider.
    In a test, we don't want to actually call the internet - we mock it.
    """
    raise NotImplementedError("This would call a real API in production.")


def calculate_total_with_shipping(cart_total: float) -> float:
    return cart_total + get_shipping_fee_from_api()


def test_total_with_mocked_shipping_fee():
    # "patch" temporarily replaces get_shipping_fee_from_api with a fake
    # version that just returns 5.0, so the test doesn't need a real API.
    with patch(
        "test_phase11_calculator.get_shipping_fee_from_api",
        return_value=5.0,
    ):
        assert calculate_total_with_shipping(20) == 25.0