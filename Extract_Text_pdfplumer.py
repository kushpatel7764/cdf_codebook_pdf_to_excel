import pdfplumber
import os

def extract_raw_text_from_pdf(anes_pdf_path, output_file="raw_pdf.txt"):
    extracted_text = ""
    
    if os.path.exists(output_file):
        print("An extract raw text of the pdf file already exists. Please delete the file 'raw_pdf.txt' to run this function.")
        return
    
    # Open the PDF
    with pdfplumber.open(anes_pdf_path) as pdf:
        for _, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            extracted_text += f"{text}~!^&"
    
    # save the extracted text to a file
    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        print(f"Extracted text saved to {output_file}")

def extract_prepared_text_from_pdf(anes_pdf_path, output_file_path="formatted_pdf.txt"):
    extract_raw_text_from_pdf(anes_pdf_path)
    # Define input and output file paths
    input_file_path = "raw_pdf.txt"
    # Open the input file and process each line
    with open(input_file_path, "r", encoding="utf-8") as infile, open(output_file_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            index = line.find("~!^&")  # Find the index of "~!^&"
            if index != -1:
                line = line[:index]  # Keep only the part before "~!^&"
                outfile.write(line + "\n")
            else:
                outfile.write(line)  # Write the cleaned line


    print(f"Processed file saved as {output_file_path}")
