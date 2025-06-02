import re
import pandas as pd

# Function to extract IDs and sources from the file
def extract_ids_and_sources(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Regular expressions to identify IDs and sources
    id_pattern = re.compile(r'^(VCF\d{4,5}[a-zA-Z]?)')
    #source_header_pattern = re.compile(r'^Sources\s(.+)')
    source_header_pattern = re.compile(r'^Sources\s*\n*(.+)*')
    source_line_pattern = re.compile(r'^(\d{4}):\s(.+)')
    
    # Data storage
    extracted_data = []
    current_id = None
    current_sources = []
    collecting_sources = False  # Flag to track source collection
    
    for i, line in enumerate(lines):
        # Match ID pattern
        id_match = id_pattern.search(line)
        next_line = i + 1
        next_line = lines[next_line] if len(lines) > next_line else ""
        
        question_match_regex = re.compile(r"^Question")
        question_match = question_match_regex.search(next_line)

        if not question_match:
            second_line = i + 2
            if len(lines) > second_line:
                second_next_line = lines[second_line]
                question_match = question_match_regex.search(second_next_line)
                
        if id_match and question_match:
            # If an ID is found, save the previous ID and its sources
            if current_id:
                extracted_data.append([current_id, " ".join(current_sources) if current_sources else "No sources"])
            
            # Update current ID and reset sources
            current_id = id_match.group(1)
            current_sources = []
            collecting_sources = False  # Reset source collection flag
        
        elif current_id:
            # Match sources patterns
            source_header_match = source_header_pattern.search(line)
            source_line_match = source_line_pattern.search(line)
            
            # If a sources header is found, start collecting sources
            if source_header_match:
                if source_header_match.group(1):
                    current_sources.extend(source_header_match.group(1).split())
                collecting_sources = True  # Enable source collection
            
            # If collecting sources, keep adding source lines
            elif collecting_sources and source_line_match:
                current_sources.append(f"{source_line_match.group(1)}: {source_line_match.group(2)}")
    
    # Add the last ID and its sources to the data list
    if current_id:
        extracted_data.append([current_id, " ".join(current_sources) if current_sources else "No sources"])
    
    return extracted_data

# File path to input file
file_path = './output2.txt'
# Extract data from file
data = extract_ids_and_sources(file_path)

# Convert data to DataFrame and save as Excel file
df = pd.DataFrame(data, columns=['ID', 'Sources'])
df.to_excel('extracted_ids_sources1.xlsx', index=False)

# Print confirmation message
print("Excel file created: extracted_ids_sources.xlsx")
