import os, re
from docx import Document
from docx.shared import Inches
from ai_integration import ask_ai, get_report_building_prompt
from config import INPUT_XLSX, CHARTS_DIR
from llm_prompts import LLM_OUTPUT_SIMPLE

# Parses the LLM output in Markdown into DOCX paraghraphs
def add_markdown_paragraph(doc, text):
    """
    Adds a paragraph to the docx Document, parsing **bold** and _italic_ markdown.
    """
    p = doc.add_paragraph()

    # Regex to capture bold (**...**) and italic (*...*) markers
    tokens = re.split(r'(\*\*.*?\*\*|__.*?__|\*.*?\*|_.*?_)', text)

    for token in tokens:
        if not token:
            continue
        run = p.add_run()

        if token.startswith("**") and token.endswith("**"):
            run.text = token[2:-2]
            run.bold = True
        elif token.startswith("__") and token.endswith("__"):
            run.text = token[2:-2]
            run.bold = True
        elif token.startswith("*") and token.endswith("*"):
            run.text = token[1:-1]
            run.italic = True
        elif token.startswith("_") and token.endswith("_"):
            run.text = token[1:-1]
            run.italic = True
        else:
            run.text = token

# This function inserts the chart for a given column into the document
def insert_chart_for_column(doc, col_letter, charts_dir="charts"):
    for fname in os.listdir(charts_dir):
        if f"_column{col_letter}.jpg" in fname:
            chart_path = os.path.join(charts_dir, fname)
            doc.add_picture(chart_path, width=Inches(5.5))
            return True
    return False

# This function generates a .DOCX report by leveraging LLM
def generate_diagnosis_report():
    prompt = get_report_building_prompt()
    print(f"LLM PROMPT:\n{prompt}\n")

    # Comment for testing to not spend AI Tokens
    #outline = ask_ai(prompt)
    #print(f"LLM Output:\n{outline}")
    outline = LLM_OUTPUT_SIMPLE

    doc = Document()
    doc.add_heading("Roteiro de Diagnóstico de Internacionalização", level=0)

    for line in outline.split("\n"):
        if line.strip() == "":
            continue

        if line.startswith("# "):
            doc.add_heading(line[2:], level=1)

        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)

        elif line.startswith("### "):
            doc.add_heading(line[4:], level=3)

        else:
            # Parses the LLM Markdown output and inserts into the document
            clean_line = line.strip()
            add_markdown_paragraph(doc, clean_line)

            # Matches the placeholder for charts - so we can include it into the document
            col_match = re.match(r"[-•\s]*\*{0,2}([A-Z]{1,3})\*{0,2}\s*[:—\-–]", clean_line)
            if col_match:
                col_letter = col_match.group(1)
                inserted = insert_chart_for_column(doc, col_letter)
                if not inserted:
                    print(f"(No chart found for column {col_letter})")

    # build the report path
    base_name = os.path.splitext(os.path.basename(INPUT_XLSX))[0]
    report_path = os.path.join(os.path.dirname(INPUT_XLSX), f"{base_name}_report.docx")

    # remove existing file if present
    if os.path.exists(report_path):
        os.remove(report_path)

    # Saves the report
    doc.save(report_path)
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    generate_diagnosis_report()