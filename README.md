# Survey Data Processor
This project processes survey data from a CSV file, extracts questions and answers, and generates an output CSV with aggregated responses.

## Features
- Reads a survey CSV file with a two-line header.
- Extracts questions and unique answers while ignoring specified columns.
- Calculates answer proportions and absolute counts.
- Groups excess answers into an "Others" category if the number of unique answers exceeds a threshold.
- Outputs the processed data into a structured CSV file.

## Requirements
Required libraries are listed on the `requirements.txt` file

### Build the Environment
To build the Environment inside project-root\.env

1. Create a folder named `.env`
2. Put the required libraries on the `requirements.txt` file
3. Run `pip install virtualenv`
4. Run `python -m virtualenv .env`
5. Run `source .env/Scripts/activate`
6. Run `python -m pip install -r requirements.txt`
7. Run `pip list`

## Usage
The `input.csv` file format used for this project follows this format, for each column:
- On the first line it contains a header, anything really.
- On the second line it contains an optional tag, used to identify special questions
    - e.g.: ignore, multi_choice, open_question, etc.
- From the third line onwards it contains the question answers, one per line.

