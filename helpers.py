import re
import textwrap
import pandas as pd

# This function makes sure our Excel sheet names are clean and not too long
def sanitize_sheet_name(name, existing):
    # Replace any weird characters with "_"
    clean = re.sub(r'[\[\]\:\*\?\/\\]', "_", str(name))[:31] or "Sheet"

    # If the name already exists, add a number to make it unique
    base = clean
    i = 1
    while clean in existing:
        tail = f"_{i}"
        
        # Make sure the name doesn't go over 31 characters
        clean = (base[:(31 - len(tail))] + tail) if len(base) + len(tail) > 31 else base + tail
        i += 1

    return clean

# This function makes safe filenames for saving pictures
def sanitize_filename(s, max_len=140):
    s = str(s)
    
    # Replace weird characters with "_"
    s = re.sub(r'[^\w\-\.\(\) ]+', '_', s)
    
    # Replace spaces with "_" and remove extras
    s = re.sub(r'\s+', '_', s).strip('_')
    
    # Make sure the name isn’t too long
    return s[:max_len] if len(s) > max_len else s

# This function turns a column number into Excel-style letters (like A, B, C, ..., AA)
def colnum_to_excel(n: int) -> str:
    string = ""
    n += 1  # Excel starts counting from 1, not 0
    while n > 0:
        n, r = divmod(n - 1, 26)
        string = chr(65 + r) + string  # Turn numbers into letters
    return string

# This function wraps long labels so they don’t look messy in charts
def wrap_labels(labels, wrap_width=50, max_chars=150):
    wrapped = []
    for label in labels:
        label = str(label)  # Make sure it's a string
        
        # If it's too long, cut it and add "..."
        if len(label) > max_chars:
            label = label[:max_chars].rstrip() + "..."
        
        # Break the label into lines so it fits nicely
        wrapped.append('\n'.join(textwrap.wrap(label, wrap_width)))
    return wrapped