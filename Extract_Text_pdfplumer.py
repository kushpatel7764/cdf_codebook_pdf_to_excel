import pdfplumber
import os
from PIL import Image

def extract_text_from_pdf(pdf_path, output_file="output1.txt"):
    extracted_text = ""

    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            extracted_text += f"{text}~!^&"
    
    # save the extracted text to a file
    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        print(f"Extracted text saved to {output_file}")


#extract_text_from_pdf("TableSourceFinal.pdf")


# Define input and output file paths
input_file = "output1.txt"
output_file = "output2.txt"
# Open the input file and process each line
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        index = line.find("~!^&")  # Find the index of "~!^&"
        if index != -1:
            line = line[:index]  # Keep only the part before "~!^&"
            outfile.write(line + "\n")
        else:
            outfile.write(line)  # Write the cleaned line


print(f"Processed file saved as {output_file}")
