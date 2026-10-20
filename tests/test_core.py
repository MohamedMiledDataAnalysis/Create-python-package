"""Tests, run with `pytest`: the equivalent of tests/testthat/ in R."""

import pytest

from finbasic import loan_payment, npv


def test_loan_payment():
    assert loan_payment(200_000, 0.045, 25) == pytest.approx(1111.66, abs=0.005)


def test_loan_payment_zero_rate():
    assert loan_payment(12_000, 0, 1) == pytest.approx(1_000)


def test_loan_payment_rejects_bad_input():
    with pytest.raises(ValueError):
        loan_payment(-1, 0.05, 10)


def test_npv():
    assert npv(0.10, [-1000, 300, 400, 500]) == pytest.approx(-21.04, abs=0.005)
