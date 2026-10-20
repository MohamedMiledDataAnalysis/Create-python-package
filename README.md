# finbasic: a basic Python package, explained

`finbasic` contains two financial functions:

- `loan_payment(principal, rate, years)`: monthly payment of a fixed-rate loan
- `npv(rate, cash_flows)`: net present value of a series of cash flows

This README explains every file of the package, then every step of the
process: from writing the code to sharing the package.

---

## Part 1: The files

```
finbasic/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── finbasic/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

Two folders, two kinds of content:

- `src/finbasic/` holds the code that users install.
- `tests/` holds the code that checks it. It is not installed.

### 1.1 `pyproject.toml`: the package description

This file tells `pip` what the package is and how to build it.
Without it, the folder is just code; with it, the folder is a package.

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
```

- `[build-system]` names the tool that turns the code into an
  installable file. `setuptools` is the standard choice.
- `pip` downloads this tool automatically during installation.

```toml
[project]
name = "finbasic"
version = "0.1.0"
description = "Basic financial functions: loan payment and net present value."
readme = "README.md"
license = "MIT"
authors = [{ name = "Mohamed Miled" }]
requires-python = ">=3.10"
dependencies = []
```

| Field | Meaning |
|---|---|
| `name` | the name used in `pip install finbasic` |
| `version` | MAJOR.MINOR.PATCH; increase it at each release |
| `description` | one line, shown in `pip show finbasic` |
| `readme` | the long description, shown on PyPI |
| `license` | the licence, as a standard identifier |
| `requires-python` | the oldest Python version supported |
| `dependencies` | other packages pip must install with this one |

`dependencies` is empty because the two functions use only plain Python.
If the package needed pandas, you would write `dependencies = ["pandas>=2.1"]`
and pip would install pandas automatically.

```toml
[project.optional-dependencies]
dev = ["pytest>=8.0"]
```

- Packages needed only by the developer, not by users.
- They are installed only on request: `pip install -e ".[dev]"`.

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

- Tells setuptools that the code lives in the `src/` folder.

### 1.2 The `src/` folder: why the extra level

The code could sit directly in `finbasic/finbasic/`. Putting it in
`src/finbasic/` is the recommended layout:

- Python cannot import the package straight from the project folder.
- So the tests always run against the **installed** package.
- A file missing from the installation then fails the tests,
  instead of failing later for your users.

### 1.3 `src/finbasic/__init__.py`: the front door

```python
"""finbasic: basic financial functions."""

from .core import loan_payment, npv

__version__ = "0.1.0"
__all__ = ["loan_payment", "npv"]
```

- Its presence turns the folder `finbasic/` into a package.
- Python runs it when a user writes `import finbasic`.
- `from .core import ...` brings the functions up from `core.py`.
  The dot means "from this package".
- Users can then write `finbasic.npv(...)` rather than
  `finbasic.core.npv(...)`.
- `__version__` lets users check the version: `finbasic.__version__`.
- `__all__` lists the public functions: those imported by
  `from finbasic import *`.

### 1.4 `src/finbasic/core.py`: the functions

```python
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
        raise ValueError(
            "principal and years must be positive, rate must be 0 or more"
        )
    n = years * 12
    r = rate / 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)
```

| Part | Role |
|---|---|
| `principal: float` | type hint: documents the expected type; Python does not enforce it |
| `-> float` | type hint for the returned value |
| `"""..."""` | the docstring: the help text shown by `help(loan_payment)` |
| `>>>` lines | an example; pytest can run it to prove the documentation is correct |
| `raise ValueError(...)` | stops with a clear message on invalid input |
| `if r == 0` | handles an interest-free loan, where the formula would divide by zero |

`npv` follows the same pattern. `enumerate(cash_flows)` returns each cash
flow with its position (0, 1, 2...), which is the period used for discounting.

### 1.5 `tests/test_core.py`: the tests

```python
import pytest

from finbasic import loan_payment, npv


def test_loan_payment():
    assert loan_payment(200_000, 0.045, 25) == pytest.approx(1111.66, abs=0.005)


def test_loan_payment_rejects_bad_input():
    with pytest.raises(ValueError):
        loan_payment(-1, 0.05, 10)
```

pytest works by naming conventions:

- it runs every file named `test_*.py`;
- in each file, it runs every function named `test_*`;
- a test passes if its `assert` is true, and fails otherwise.

Two tools appear here:

- `pytest.approx` compares decimals with a tolerance. Computers store
  decimals with tiny rounding errors, so `==` alone is unreliable.
- `pytest.raises(ValueError)` checks that the code **does** raise
  the error. The test fails if no error occurs.

### 1.6 `README.md` and `LICENSE`

- `README.md` is this file: the documentation shown on GitHub and PyPI.
- `LICENSE` holds the MIT licence: anyone may use, copy and modify the
  code, provided the copyright notice is kept.

---

## Part 2: The process, step by step

### Step 1: Create a virtual environment

A virtual environment is a separate Python installation for one project.
Packages installed in it do not affect your other projects.
It plays the role of `renv` in R.

```bash
cd finbasic
python -m venv .venv
```

Activate it (every time you open a new terminal):

```bash
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

The terminal prompt now starts with `(.venv)`.

### Step 2: Write the code

- Put the functions in `src/finbasic/core.py`.
- Export them in `src/finbasic/__init__.py`.
- Describe the package in `pyproject.toml`.

### Step 3: Install the package in editable mode

```bash
pip install -e ".[dev]"
```

- `-e` (editable) links the installation to your folder: each change
  to the code applies immediately, without reinstalling.
  This is the equivalent of `devtools::load_all()` in R.
- `.` means "the package in this folder".
- `[dev]` also installs the development tools listed in `pyproject.toml`
  (here, pytest).

### Step 4: Run the tests

```bash
pytest
```

Expected output:

```
....                                                       [100%]
4 passed in 0.02s
```

Each dot is a passing test. A failing test shows `F` and the details.

To also run the `>>>` examples in the docstrings:

```bash
pytest --doctest-modules src tests
```

### Step 5: Use the package

From any script or Python session, in the same environment:

```python
import finbasic as fb

fb.loan_payment(200_000, 0.045, 25)    # 1111.66...
fb.npv(0.10, [-1000, 300, 400, 500])   # -21.04...
help(fb.loan_payment)                  # shows the docstring
```

### Step 6: Release a new version

1. Change the code.
2. Run `pytest`.
3. Increase the version in **both** `pyproject.toml` and `__init__.py`:
   - `0.1.0` → `0.1.1` for a bug fix;
   - `0.1.0` → `0.2.0` for a new function;
   - `0.1.0` → `1.0.0` for a change that breaks existing code.

### Step 7: Build the distribution files

```bash
pip install build
python -m build
```

This creates a `dist/` folder with two files:

| File | Content |
|---|---|
| `finbasic-0.1.0-py3-none-any.whl` | the wheel: ready to install, the format pip prefers |
| `finbasic-0.1.0.tar.gz` | the source distribution: the code plus `pyproject.toml` |

In the wheel name, `py3-none-any` means: any Python 3, no compiled code,
any operating system.

### Step 8: Share the package

**Option A: send the wheel.** The recipient runs:

```bash
pip install finbasic-0.1.0-py3-none-any.whl
```

**Option B: GitHub.** Push the folder to a repository; anyone installs with:

```bash
pip install git+https://github.com/YOUR-USERNAME/finbasic.git
```

**Option C: PyPI**, the public index, so that `pip install finbasic`
works everywhere:

1. Check the name is free on [pypi.org](https://pypi.org).
2. Create accounts on [test.pypi.org](https://test.pypi.org) and
   [pypi.org](https://pypi.org), with an API token on each.
3. Upload to the test index first, then to the real one:
   ```bash
   pip install twine
   twine upload --repository testpypi dist/*
   twine upload dist/*
   ```

PyPI does not review packages, unlike CRAN: the tests are your quality check.
PyPI also refuses to replace an existing version: each upload needs a new
version number.

---

## Part 3: Common problems

| Message | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'finbasic'` | the package is installed in another environment | activate `.venv`, then `pip install -e .` |
| `ImportError: cannot import name 'npv'` | the function is missing from `__init__.py` | add it to the `from .core import ...` line |
| A code change has no effect | the package was installed without `-e` | reinstall with `pip install -e .` |
| `File 'README.md' cannot be found` during the build | `readme` in `pyproject.toml` points to a missing file | create the file or remove the line |
