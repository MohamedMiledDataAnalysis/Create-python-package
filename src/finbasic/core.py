"""The package functions: the equivalent of the R/ folder in R."""


def loan_payment(principal: float, rate: float, years: int) -> float:
    """Monthly payment of a fixed-rate loan.

    Args:
        principal: amount borrowed.
        rate: annual interest rate as a decimal (0.045 for 4.5%).
        years: term of the loan in years.

    Returns:
        The fixed monthly payment.

    Example:
        >>> round(loan_payment(200_000, 0.045, 25), 2)
        1111.66
    """
    if principal <= 0 or years <= 0 or rate < 0:
        raise ValueError("principal and years must be positive, rate must be 0 or more")
    n = years * 12
    r = rate / 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def npv(rate: float, cash_flows: list[float]) -> float:
    """Net present value of cash flows, the first one occurring today.

    Args:
        rate: discount rate per period (0.10 for 10%).
        cash_flows: one value per period, starting at period 0.

    Returns:
        The value today of all the cash flows.

    Example:
        >>> round(npv(0.10, [-1000, 300, 400, 500]), 2)
        -21.04
    """
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
