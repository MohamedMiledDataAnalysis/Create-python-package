# finbasic (Python)

Basic financial functions: loan payment and net present value.

## Install

```bash
pip install .            # from this folder
pip install -e ".[dev]"  # editable, with pytest, while developing
```

## Use

```python
import finbasic as fb

fb.loan_payment(200_000, 0.045, 25)    # 1111.66
fb.npv(0.10, [-1000, 300, 400, 500])   # -21.04
help(fb.loan_payment)                  # documentation
```

## Test

```bash
pytest
```
