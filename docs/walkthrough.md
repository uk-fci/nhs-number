---
title: Walkthrough
authors: Dr Marcus Baw
---

# Walkthrough

A guided tour of everything the library does, in the order you are likely to need it. Every block below is copy-pastable into a Python REPL, and **every output shown is the real output** - captured from a session against version 2.1.0.

!!! tip "Reproducing the generated numbers exactly"
    `generate()` returns random numbers, so it would normally differ every run. The examples that generate numbers call `random.seed(...)` first, so if you paste the blocks as written you will get exactly the numbers shown here.

## 1. Install it

```bash
pip install nhs-number
```

```python
import nhs_number
```

Everything below assumes you have imported the names as you go, so each block stands alone.

## 2. Is this NHS number valid?

The single most common thing you want. `is_valid()` returns a plain `True` or `False`.

```python
from nhs_number import is_valid

is_valid('9876543210')
# True

is_valid('1234567890')
# False
```

Validity here means the number is ten digits and its final digit is the correct **check digit** under the NHS Modulus 11 algorithm. That catches the overwhelming majority of typos and transcription errors.

## 3. It copes with messy input

Real-world numbers arrive formatted, or as integers, or as junk from a spreadsheet. `is_valid()` handles all of it, and **never raises** - anything it cannot make sense of is simply invalid.

```python
from nhs_number import is_valid

is_valid('987 654 3210')
# True

is_valid('987-654-3210')
# True

is_valid(9876543210)
# True

is_valid('')
# False

is_valid(None)
# False

is_valid('banana')
# False
```

That last group matters: you can pass a whole column of dirty data through `is_valid()` without wrapping it in `try`/`except`.

## 4. Cleaning a number up

To store or compare numbers, normalise them to the bare ten digits first.

```python
from nhs_number import normalise_number, standardise_format

normalise_number('987 654 3210')
# '9876543210'

standardise_format('987-654-3210')
# '9876543210'

standardise_format('nonsense')
# ''
```

`normalise_number()` and `standardise_format()` are the same function under two names. Anything unparseable returns the empty string, which is falsy - so `if standardise_format(x):` is a neat way to filter a messy column.

## 5. Which part of the UK is it from?

Ranges of NHS numbers are allocated to different parts of the UK and Ireland. Pass `for_region=` to require that a number falls inside one.

```python
from nhs_number import is_valid, REGION_ENGLAND

is_valid('4000000632', for_region=REGION_ENGLAND)
# True

is_valid('9876543210', for_region=REGION_ENGLAND)
# False
```

The second number has a perfectly good check digit - it is simply not in the England/Wales/Isle of Man range. The available regions:

```python
from nhs_number import REGIONS

sorted(REGIONS)
# ['EIRE', 'ENGLAND_WALES_IOM', 'NORTHERN_IRELAND', 'RESERVED', 'SCOTLAND', 'SYNTHETIC', 'UNALLOCATED']
```

## 6. Scotland: CHI numbers carry a date of birth

A Scottish CHI number is not opaque. Its first six digits are the patient's date of birth as `DDMMYY`, so a CHI number containing an impossible date is not a valid CHI number - and the library checks this automatically, with no extra argument.

```python
from nhs_number import is_valid

is_valid('0101011113')
# True

is_valid('0113011113')
# False
```

Both numbers have a valid check digit. The second is rejected because `011301` claims a **13th month**.

## 7. Optionally, check the CHI number's sex too

A CHI number's 9th digit also encodes sex, by parity - odd for male, even for female. `is_valid()` never checks this unless you ask it to.

```python
from nhs_number import is_valid

is_valid('0101011113', sex='male')
# True

is_valid('0101011113', sex='female')
# False
```

Both numbers above are the same CHI number - only the expected sex differs. It only ever affects the result for an actual CHI number and a determinate `"male"`/`"female"` value; everything else (a non-CHI number, `"indeterminate"`, `"not_known"`, or omitting `sex` entirely) leaves the result unchanged. See [Sex and gender in this library](sex-and-gender.md) for the full reasoning, including why the parameter is called `sex` rather than `gender`.

## 8. Getting the details, not just true/false

When you want to know *why*, use the `NhsNumber` object.

```python
from nhs_number import NhsNumber

n = NhsNumber('9876543210')

n.nhs_number
# '9876543210'

n.identifier_digits
# '987654321'

n.check_digit
# 0

n.valid
# True

n.calculated_checksum
# 0

n.region_comment
# 'Not to be issued (Synthetic/test patients PDS)'
```

Comparing `check_digit` with `calculated_checksum` shows you exactly where a number went wrong. A number outside every known range reports that rather than failing:

```python
from nhs_number import NhsNumber

bad = NhsNumber('0000000005')

bad.region
# None

bad.region_comment
# 'Number did not match a known NHS number range'
```

## 9. Generating numbers for testing

Need test data? `generate()` produces valid numbers - and **by default it only draws from the synthetic/test range**, so a generated number can never collide with a real patient's.

```python
import random
from nhs_number import generate

random.seed(0)

generate()
# ['9813847336']
```

```python
import random
from nhs_number import generate

random.seed(0)

generate(quantity=3)
# ['9813847336', '9043469777', '9548977044']
```

You can confirm the safety guarantee for yourself:

```python
import random
from nhs_number import generate, REGION_SYNTHETIC

random.seed(0)

REGION_SYNTHETIC.contains_number(generate()[0])
# True
```

Ask for a specific region if you need one. Scottish numbers come out with a real date of birth built in:

```python
import random
from nhs_number import generate, REGION_SCOTLAND

random.seed(42)

generate(for_region=REGION_SCOTLAND, quantity=2)
# ['1609750403', '2603392980']
```

And you can generate deliberately **invalid** numbers, which is exactly what you want for testing your own error handling:

```python
import random
from nhs_number import generate, is_valid

random.seed(7)

generate(valid=False)
# ['9161973066']
```

```python
import random
from nhs_number import generate, is_valid

random.seed(7)

is_valid(generate(valid=False)[0])
# False
```

!!! warning "Only `for_region=REGION_SYNTHETIC` is guaranteed safe"
    The default is the synthetic range, which is safe. But if you explicitly ask for a live region - England, Scotland, Northern Ireland - you will get numbers from a range that real patients are issued from. Never use those against live systems.

## 10. Disguising real numbers

New in 2.1.0. `disguise()` turns a real number into a fake one that is still structurally valid, deterministically - the same number and seed always give the same fake, so a dataset stays internally consistent.

```python
from nhs_number import disguise

disguise('4000000632', seed=1)
# '9869172326'

disguise('4000000632', seed=1)
# '9869172326'
```

Same input, same seed, same answer - so a patient appearing in two files is disguised to the same fake number in both. Change the seed to get a different mapping:

```python
from nhs_number import disguise

disguise('4000000632', seed=2)
# '9451424865'
```

The fake is always a genuinely valid number, drawn from the synthetic range for NHS numbers:

```python
from nhs_number import disguise, is_valid

is_valid(disguise('4000000632', seed=1))
# True
```

CHI numbers are disguised into CHI-shaped numbers, with a **different, randomly chosen date of birth**:

```python
from nhs_number import disguise

disguise('0101011113', seed=1)
# '0603129978'
```

The date is deliberately not preserved - a date of birth is identifying in its own right, so keeping it would undermine the point.

!!! warning "Disguising is not anonymisation"
    The mapping is one-way (you cannot recover the original from the fake and the seed), but anyone holding **both** your seed and your original data can reproduce it. Treat the seed as a secret, and treat disguised data according to your own information-governance rules.

## 11. Recap

| You want to… | Use |
| --- | --- |
| check a number | `is_valid(number)` |
| check it belongs to a region | `is_valid(number, for_region=REGION_X)` |
| check a CHI number's sex digit | `is_valid(number, sex="male")` |
| tidy a number for storage | `normalise_number(number)` |
| find out *why* it failed | `NhsNumber(number)` |
| make safe test numbers | `generate()` |
| make test numbers that fail | `generate(valid=False)` |
| de-identify real numbers | `disguise(number, seed=...)` |

## Where next

- [Usage](usage.md) - the full reference for every function and argument
- [About NHS Numbers](nhs-numbers.md) - the number ranges and the check-digit algorithm
- [Contributing](contributing.md) - if you would like to help
