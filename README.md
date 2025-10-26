# DarkAndDarker-Exporter

A comprehensive data extraction pipeline for Dark and Darker that downloads game files, creates a mapping file, and exports game assets to JSON format.

## Overview

todo

## Process Details

todo

# Installation

## Options

### Command Line Argument Usage

For each option, the command line argument may be used at runtime instead of providing it in the `.env`.

```bash
python src/run.py                       # Run all steps with default/env values
python src/run.py --log-level INFO      # Run all steps with default/env values, except with LOG_LEVEL INFO
```

### Parameters

Copy `.env.example` to `.env` and configure the following parameters, unless they will be provided as arguments at runtime:

<!-- BEGIN_GENERATED_OPTIONS -->

<!-- END_GENERATED_OPTIONS -->

### Miscellaneous Option Behavior

* An option's value is determined by the following priority, in descending order
  * Argument
  * Option
  * Default
* If all options prefixed with `SHOULD_` are defaulted to `False`, they are instead all defaulted to `True` for ease of use
* Options are only required if their section's `SHOULD_` option is `True`

## Disclaimer

This tool is for educational and research purposes. Ensure you comply with the terms of service of Dark and Darker and Steam when using this software.