import pdfplumber
import pandas as pd
import re

pdf_path = "Test1.pdf"  
output_path = "extracted_tables1.xlsx"
text_file_path = "output.txt"  

# Read the text file
with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.readlines()

# Initialize storage lists
ids, questions, weights, notes, sources = [], [], [], [], []

# Temporary variables to store current data
current_id = None
current_question = ""
current_weights = ""
current_notes = ""
current_sources = ""
in_notes_section = False

# Process each line
for line in text:
    line = line.strip()

    # Detect new ID (lines starting with 'VCF' or similar identifiers)
    if re.match(r"VCF\d{2,}", line):  
        if current_id:  # Save the previous entry before starting a new one
            ids.append(current_id)
            questions.append(current_question.strip())
            weights.append(current_weights.strip())
            notes.append(current_notes.strip())
            sources.append(current_sources.strip())
        
        current_id = line.split()[0]  # Capture ID
        current_question, current_weights, current_notes, current_sources = "", "", "", ""  # Reset fields
        in_notes_section = False

    # Capture question-related lines
    elif line.lower().startswith("question"):
        current_question += " " + line.replace("Question", "").strip()
        in_notes_section = False
    
    # Capture weight-related lines
    elif line.lower().startswith("weight"):
        current_weights += " " + line.replace("Weight", "").strip()
        in_notes_section = False
    
    # Capture note-related lines
    elif "notes" in line.lower() or "general note" in line.lower():
        current_notes += " " + line.replace("Notes", "").replace("GENERAL NOTE:", "").strip()
        in_notes_section = True
    elif in_notes_section:
        current_notes += " " + line.strip()
    
    # Capture source lines (lines that look like "1958: V580003")
    elif re.match(r"\d{4}:\s*V\d+", line):
        current_sources += " " + line.strip()
        in_notes_section = False

# Append last collected data
if current_id:
    ids.append(current_id)
    questions.append(current_question.strip())
    weights.append(current_weights.strip())
    notes.append(current_notes.strip())
    sources.append(current_sources.strip())

# Store extracted data in a DataFrame
df = pd.DataFrame({"ID": ids, "Question": questions, "Weight": weights, "Notes": notes, "Sources": sources})

# Save to an Excel file
df.to_excel(output_path, index=False)

print("Data extracted and saved successfully.")
