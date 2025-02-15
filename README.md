# Survey Data Processor
This project processes survey data from a CSV file, extracts questions and answers, and generates an output CSV with aggregated responses.

## Features
- Reads a survey CSV file with a two-line header.
- Extracts questions and unique answers while ignoring specified columns.
- Calculates answer proportions and absolute counts.
- Groups excess answers into an "Others" category if the number of unique answers exceeds a threshold.
- Outputs the processed data into a structured CSV file.

## Requirements
- Python 3.x
- `pandas`
- `csv`

Install dependencies (if needed):
```bash
pip install pandas