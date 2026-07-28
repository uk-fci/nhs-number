# nhs-number

Python package to provide utilities for NHS Numbers, including validity checks, normalisation, and generation.

## Package Information

<table>
    <tr>
        <td>License</td>
        <td><img src="https://img.shields.io/pypi/l/nhs-number" alt="Licence type badge"></td>
        <td>Version</td>
        <td><img src="https://img.shields.io/pypi/v/nhs-number" alt="Version badge"></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/nhs-number.svg'></td>
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
</table>

## Documentation

All documentation is available at <https://uk-fci.github.io/nhs-number/>

Please note that since the demise of the Faculty of Clinical Informatics, the domain `uk-fci.tech` has been removed from the package and replaced with `uk-fci.github.io`. This is a temporary measure until we decide what to do with the `uk-fci` GitHub organisation.


## Implementing this in another language?

Please do - and you are welcome to build on our work. We publish a language-agnostic [test vector file](tests/vectors/nhs_number_cases.json) capturing how this library behaves (checksums, standardisation, validity, CHI date-of-birth rules, regions and range boundaries), so a port in any language can check itself against the same definition of correct.

It is MIT licensed, like the rest of the project: **use it freely, no permission needed.** Attribution is appreciated but not required. See [Implementing an NHS Numbers package in other languages](https://uk-fci.github.io/nhs-number/other-languages/) for what the vectors cover, what is deliberately left out and why, and how to use them.

## Changelog

<https://uk-fci.github.io/nhs-number/>
