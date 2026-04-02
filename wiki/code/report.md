# Code: `report.py`

## Purpose

Generate a PDF report that merges plots and statistical summaries.

## Components

- `add_text_page(...)`: text-only pages with wrapped line flow.
- `add_image_page(...)`: single image per page with caption.
- `summary_lines(...)`: compact formatting for summary tables.
- `build_report(...)`: orchestrates full report from generated CSVs and figures.

## Mode awareness

- `scientific`: detailed metric explanations and richer tables.
- `clean`: concise summaries.
