---
title: About NHS Numbers
authors: Dr Marcus Baw, Matt Stibbs
---

## What is an NHS Number?

The NHS Number is a single patient identifier used across the NHS. In the various UK Nations, it is referred to by different terminology and may have different validation rules.

### How do I find out my NHS Number?

Identifying individual NHS Numbers is outside the scope of this package. Still, if you are curious, you can find out your NHS number here [NHS website](https://www.nhs.uk/nhs-services/online-services/find-nhs-number/) for patients in England, Wales and the IOM, and here [NHS Scotland](https://www.nhsinform.scot/care-support-and-rights/nhs-services/nhs-number) for patients in Scotland.

### England, Wales and the Isle of Man

The NHS Number is a single patient identifier used across the NHS in England, Wales, and the Isle of Man.

In 2015, the NHS Number was legally mandated to be used as a single patient identifier across health and care with the introduction of the [The Health and Social Care (Safety and Quality) Bill](https://www.digitalhealth.net/2015/10/nhs-number-use-becomes-law/).

The use of the NHS number in health and care organisations in England is specified in the [Information Standards Board](https://digital.nhs.uk/data-and-information/information-standards) standard [ISB 0149 NHS Number](https://digital.nhs.uk/data-and-information/information-standards/information-standards-and-data-collections-including-extractions/publications-and-notifications/standards-and-collections/isb-0149-nhs-number) (Note that these NHS Digital links, while live at the time of editing this documentation, may at some stage move to NHS England following the merger of those organisations, which is ongoing, in 2023)

### Scotland

Scotland calls the identifier a Community Health Index (CHI) Number, using a similar standard for check-digit validation. However, the first 6 digits of the number are the date of birth in the format `DDMMYY` rather than a sequential number. Following this, there is a 3-sequence number.

The ninth digit is always even for females and odd for males.

### Northern Ireland

Northern Ireland has similar single patient identifiers, referred to as the Health and Care Number (H&C Number).

### Republic of Ireland

While the Republic of Ireland is its own sovereign state, independent from the UK, using its own Individual Health Identifier (IHI) number, it is included here for completeness because the IHI _internally_ uses the range of identifiers reserved for it as per the table below and the NHS Number may possibly be used in cross-border care.

For more detail, see [Individual Health Identifier (IHI)](./ihi-ireland.md).

## NHS Number Ranges

### Live NHS Number Ranges

This table shows how different ranges within the standard number format are distributed across the UK and Ireland.

`n` represents a digit, `0-9`, which is the check digit.

| <div style="width:200px">Range</div> | Usage               | Description                                                                                                                                                                                            |
| ------------------------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 010000000n - 319999999n              | Scotland            | Used for Scottish [Community Health Index (CHI)](<https://en.wikipedia.org/wiki/Community_Health_Index_(Scotland)>) numbers, which have historically contained the date of birth as the first 6 digits. |
| 320000000n - 399999999n              | Northern Ireland    | Used for NI Health and Care Numbers.                                                                                                                                                                   |
| 400000000n - 499999999n              | England, Wales, IOM | Used for NHS numbers in England, Wales and the Isle of Man.                                                                                                                                            |
| 600000000n - 799999999n              | England, Wales, IOM | Used for NHS numbers in England, Wales and the Isle of Man.                                                                                                                                            |
| 800000000n - 859999999n              | Republic of Ireland | Used by the Republic of Ireland within the IHI (digits 8-17).                                                                                                                                          |

### Test/Unallocated Number Ranges

This table shows the ranges not assigned to live use (e.g. testing, unallocated).

| <div style="width:200px">Range</div> | Usage   | Description                                                   |
| ------------------------------------ | ------- | ------------------------------------------------------------- |
| 500000000n - 599999999n              | Testing | Used for NHS Care Records Service internal testing.           |
| 860000000n - 899999999n              | Spare   | Unallocated range to allow for future expansion.              |
| 900000000n - 999999999n              | Testing | Unallocated and Development / Test systems to use this range. |

## NHS Number Check Digit Validation

NHS Numbers in England, Wales and the Isle of Man are a simple 9-digit number with a check digit. The check digit is calculated using a variation of the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm) (also known as the [Modulus 11 algorithm](https://en.wikipedia.org/wiki/Check_digit#Modulus_11)).

This check digit is intended to make the number somewhat resistant to accidental transcription errors, not to make it cryptographically secure.

### Information Sources

- [Wikipedia: NHS numbers](https://en.wikipedia.org/wiki/NHS_number)

- [NHS Numbers and the systems used to manage them - An overview for research users](https://www.closer.ac.uk/wp-content/uploads/CLOSER-NHS-ID-Resource-Report-Apr2018.pdf)

- [CHI Numbers reference](https://www.ndc.scot.nhs.uk/Data-Dictionary/SMR-Datasets/Patient-Identification-and-Demographic-Information/Community-Health-Index-Number/)

- [Individual Health Identifier (IHI) for Ireland](https://www.hse.ie/eng/about/who/national-services/individual-health-identifier/)

### Further reading

For those with an unnaturally strong interest in the NHS Number, you may enjoy the following:

- [blu3id's Three Word NHS Number POC](https://blu3id.uk/posts/three-word-nhs-number)
