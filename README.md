# nhs-number

Python package to provide utilities for NHS Numbers, including validity checks, normalisation, and generation.

This package is a collaboration between a number of individuals, groups and teams, who were each separately maintaining some kind of NHS Number Python package. See [Acknowledgements](#acknowledgements) for more information.

## Package Information

<table>
    <tr>
        <td>License</td>
        <td><img src="https://img.shields.io/pypi/l/nhs-number" alt="Licence type badge"></td>
        <td>Version</td>
        <td><img src="https://img.shields.io/pypi/v/nhs-number" alt="Version badge"></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://www.travis-ci.com/andylaw/NhsNumberChecks.svg?branch=main'></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/andylaw/NhsNumberChecks/branch/main/graph/badge.svg'></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/nhs-number'></td>
        <td>Implementation</td>
        <td><img src='https://img.shields.io/pypi/implementation/nhs-number'></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/nhs-number'></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/nhs-number'></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/nhs-number.svg'></td>
    </tr>
</table>

## Installation

```bash
pip install nhs-number
```

## Basic Usage

Provides a set of tools to handle NHS numbers, mainly validation and normalisation of the number, and generation of numbers for testing. IMPORTANT: **You should never need to generate an NHS Number for a live system**. Live numbers are always generated in some kind of central registry, such as the NHS Spine in England, and they are assigned to patients.

```python
import nhs_number

nhs_number.is_valid('1234567890')
# False

nhs_number.is_valid('1234567891')
# True

nhs_number.standardise_format('123 456 7891')
# '1234567891'
```

---

## What is an NHS Number?

The NHS Number is a single patient identifier used across the NHS in England, Wales, and the Isle of Man.

In 2015, the NHS Number was legally mandated to be used as a single patient identifier across health and care with the introduction of the [The Health and Social Care (Safety and Quality) Bill](https://www.digitalhealth.net/2015/10/nhs-number-use-becomes-law/).

Scotland and Northern Ireland have similar single patient identifiers, on which there is more information below.

## Using the NHS number within services and systems

The use of the NHS number in health and care organisations is specified in an the [Information Standards Board](https://digital.nhs.uk/data-and-information/information-standards) standard [ISB 0149 NHS Number](https://digital.nhs.uk/data-and-information/information-standards/information-standards-and-data-collections-including-extractions/publications-and-notifications/standards-and-collections/isb-0149-nhs-number)

These identifiers are referred to by different devolved nations with different terminology:

* Health and Care Number ("H&C Number") in Northern Ireland
* Community Health Index ("CHI Number") in Scotland


### Live Number Ranges

This tables shows how different ranges within the standard number format are distributed across the UK and Ireland.

| Range                 | Where Used       | Description                                                                                                                                                                                            |
| --------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 010000000n-099999999n | Scotland         | Numbers from within this range already used by the Scottish CHI system                                                                                                                                 |
| 100000000n-319999999n | Scotland         | Used for Scottish [Community Health Index (CHI)](<https://en.wikipedia.org/wiki/Community_Health_Index_(Scotland)>) numbers, which have historically contained the date of birth as the first 6 digits |
| 320000000n-399999999n | Northern Ireland | Used for NI Health and Care Numbers                                                                                                                                                                    |
| 400000000n-499999999n | England & Wales  | Used for [NHS numbers](https://en.wikipedia.org/wiki/NHS_number) in England & Wales                                                                                                                    |
| 600000000n-799999999n | England & Wales  | Used for [NHS numbers](https://en.wikipedia.org/wiki/NHS_number) in England & Wales                                                                                                                    |
| 800000000n-859999999n | Ireland          | Used by the Republic of Ireland                                                                                                                                                                        |

### Test Number Ranges

This tables shows the ranges not assigned to live use (e.g. testing, unallocated)

| Range                 | Where Used | Description                                                  |
| --------------------- | ---------- | ------------------------------------------------------------ |
| 500000000n-599999999n | Testing    | Used for NHSCR internal testing                              |
| 860000000n-899999999n | Spare      | Unallocated range to allow for future expansion              |
| 900000000n-999999999n | Testing    | Unallocated and Development / Test systems to use this range |


## Acknowledgements

This package is a collaboration between a number of individuals, groups and teams, who were each separately maintaining some kind of NHS Number Python package. We felt that rather than having several packages with overlapping functionality, it would be better to combine our efforts into a single package.

The package has been adopted by the [Faculty of Clinical Informatics](https://www.facultyofclinicalinformatics.org.uk/), with the aim to develop it into the canonical NHS Number package for Python.

### Authors and contributors

* [Andy Law](https://github.com/andylaw) - author of the PyPi package [nhs-number](https://pypi.org/project/nhs-number/), head of research computing at The Roslin Institute

* [Matt Stibbs](https://github.com/mattstibbs) - author of [nhspy](https://pypi.org/project/nhspy/)

* [Marcus Baw](https://github.com/pacharanero) - [RCPCH](https://github.com/rcpch) developer

* [Simon Chapman](https://github.com/eatyourpeas) - [RCPCH](https://github.com/rcpch) developer

* [Anchit Chandran](https://github.com/anchit-chandran) - [RCPCH](https://github.com/rcpch) developer

* [Mark Bailey](https://github.com/Cotswoldsmaker) - Acting Chair of the [Faculty of Clinical Informatics](https://www.facultyofclinicalinformatics.org.uk/)

* [Mark Sellors](https://github.com/sellorm) - author of [nhssums](https://pypi.org/project/nhssums/)


### Information Sources and further reading

* [NHS Numbers and the systems used to manage them - An overview for research users](https://www.closer.ac.uk/wp-content/uploads/CLOSER-NHS-ID-Resource-Report-Apr2018.pdf)

* [Wikipedia: NHS numbers](https://en.wikipedia.org/wiki/NHS_number)

* [blu3id's Three Word NHS Number POC](https://blu3id.uk/posts/three-word-nhs-number)
