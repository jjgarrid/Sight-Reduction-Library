# Issue Report: LaTeX Template String Formatting Error

## Problem Description
When implementing a LaTeX template system for sight reduction worksheets, an error occurred during the string formatting process: `"unsupported format character 'P' (0x50) at index 306"`.

## Root Cause Analysis
The error occurred because:

1. We initially attempted to use Python's old-style string formatting with `%` placeholders in the LaTeX template
2. The LaTeX template contained comment lines that began with `%`, such as `% Page setup`
3. When Python's `%` string formatting tried to process the template, it interpreted `%P` as a format specifier
4. Since 'P' is not a valid format character in Python's string formatting, it threw the error

## Resolution Approach
To solve this issue, we need to avoid using Python's `%` formatting with LaTeX templates since LaTeX heavily uses the `%` character for comments. 

The proper solution is to use a different approach:
1. Either use Python's newer `.format()` method with carefully escaped placeholders
2. Or use double braces `{{variable_name}}` which become single braces `{variable_name}` after Python formatting, avoiding conflicts with LaTeX

## Technical Details
- Error: `ValueError: unsupported format character 'P' (0x50) at index 306`
- Location: In the LaTeX template string, at character index 306
- Problematic sequence: `% Page setup` in the template was interpreted as format code

## Recommended Solution
For LaTeX templates with Python, use string templates with double braces or a custom replacement function that doesn't conflict with LaTeX syntax.

## Corrections Implemented
- Made LaTeX-safe formatting in `src/latex_output.py`:
  - Escaped stray `%` not part of `%(...)s` or `%%` using regex, so LaTeX comment lines remain `%` after formatting while avoiding Python’s `%` parser.
  - Added safe substitution that supplies empty strings for missing keys to prevent `KeyError`/`ValueError` during rendering.
- Standardized placeholders in templates (`src/latex_templates.py`):
  - Replaced `{{{instrument_error}}}`/`{{{index_error}}}`/`{{{personal_error}}}` with `{{%(...)s}}` to align with the formatter.
  - Injected answer key via `%(answer_key)s` (previously `{{{answer_key}}}`), ensuring the "Answer Key" section renders.
  - Revised `ANSWER_KEY_TEMPLATE` to use `%(...)s` consistently and removed unused placeholders that were not provided by the renderer.

These changes fix the `unsupported format character` error and produce stable LaTeX output without mixing incompatible placeholder syntaxes.
