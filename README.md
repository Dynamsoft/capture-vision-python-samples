# Dynamsoft Capture Vision Samples for Python edition

[![Current version number](https://img.shields.io/pypi/v/dynamsoft_capture_vision_bundle?color=orange)](https://pypi.org/project/dynamsoft_capture_vision_bundle/)
[![Supported Python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/downloads/)
[![PyPI downloads](https://img.shields.io/pypi/dm/dynamsoft_capture_vision_bundle)](https://pypistats.org/packages/dynamsoft_capture_vision_bundle)

![Dynamsoft](https://dynamsoft.github.io/styleguide/assets/images/icons/dynamsoft_logos/dynamsoft_logo_original.png "Dynamsoft")  

## Overview

This repository contains multiple samples that demonstrate how to use the [Dynamsoft Capture Vision](https://www.dynamsoft.com/capture-vision/docs/core/introduction/?lang=python) Python Edition.

## Requirements

### Supported Platforms
- Windows x64
- Linux (x64, ARM64)
- macOS (10.15+)

### Supported Python Versions

- Python 3.14
- Python 3.13
- Python 3.12
- Python 3.11
- Python 3.10


## Installation

```
pip install dynamsoft-capture-vision-bundle
```

or 

```
pip3 install dynamsoft-capture-vision-bundle
```

## Samples

| Sample Name | Description |
| ----------- | ----------- |
|[`MRZScanner`](Samples/mrz_scanner.py)          | Capture and extract user's information from machine-readable travel documents with Dynamsoft Capture Vision SDK.            |
|[`DriverLicenseScanner`](Samples/driver_license_scanner.py)          | Capture and extract user's information from driver license/ID with Dynamsoft Capture Vision SDK.            |
|[`VINScanner`](Samples/vin_scanner.py)          | Capture and extract vehicle's information from Vehicle Identification Number (VIN) with Dynamsoft Capture Vision SDK.            |
|[`DocumentScanner`](Samples/document_scanner.py)          | The simplest way to detect and normalize a document from an image and save the result as a new image.            |
|[`GS1AIScanner`](Samples/gs1_ai_scanner.py) | Shows how to extract and interpret GS1 Application Identifiers (AIs) from GS1 barcodes. |

## Documentation

https://www.dynamsoft.com/capture-vision/docs/server/programming/python/?ver=latest&utm_source=samples

## License

The library requires a license to work, you use the API `LicenseManager.init_license` to initialize license key and activate the SDK.

These samples use a free public trial license which require network connection to function. You can request a 30-day free trial license via the <a href="https://www.dynamsoft.com/customer/license/trialLicense?product=dcv&utm_source=github&package=python" target="_blank">Request a Trial License</a> link which works offline.

## Contact Us

https://www.dynamsoft.com/company/contact/
