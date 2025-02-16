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
```

## Usage
The `input.csv` file format used for this project follows this format, for each column
- On the first line it contains a header, anything really.
- On the second line it contains an optional tag, used to identify special questions
    - e.g.: ignore, multi_choice, open_question, etc.
- From the third line onwards it contains the question answers, one per line.