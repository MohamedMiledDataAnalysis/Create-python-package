"""finbasic: basic financial functions.

What this file exports is what `import finbasic` gives the user:
the equivalent of NAMESPACE in R.
"""

from .core import loan_payment, npv

__version__ = "0.1.0"
__all__ = ["loan_payment", "npv"]
