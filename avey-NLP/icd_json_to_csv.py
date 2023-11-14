import json
import pandas as pd

# # Function to recursively traverse the JSON hierarchy and extract "name" and "desc" pairs
# def extract_diag(data, results, alt_desc_index):
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if key == 'diag':
#                 if isinstance(value, list):
#                     for item in value:
#                         if isinstance(item, dict):
#                             entry = {'name': item.get('name'), 'desc': item.get('desc')}
#                             alt_descs = []
                            
#                             # Handle 'inclusionTerm' if present
#                             inclusion_term = item.get('inclusionTerm')
#                             if inclusion_term:
#                                 note = inclusion_term.get('note')
#                                 if note:
#                                     if isinstance(note, list):
#                                         alt_descs.extend(note)
#                                     else:
#                                         alt_descs.append(note)
                            
#                             # Add alternative descriptions to the entry
#                             for i, alt_desc in enumerate(alt_descs):
#                                 entry[f'alternative desc {i+1}'] = alt_desc
#                                 alt_desc_index = max(alt_desc_index, i+1)
                            
#                             results.append(entry)
#                             extract_diag(item, results, alt_desc_index)
#                 else:
#                     print(f"Expected a list for 'diag', but found: {type(value)}")
#             else:
#                 extract_diag(value, results, alt_desc_index)
#     elif isinstance(data, list):
#         for item in data:
#             extract_diag(item, results, alt_desc_index)

# # Load the JSON file
# with open('icd10cm_tabular_2024.json', 'r') as file:
#     json_data = json.load(file)

# # Initialize the results list and the maximum index of alternative descriptions
# results = []
# max_alt_desc_index = 0

# # Start the recursive extraction
# extract_diag(json_data, results, max_alt_desc_index)

# # Create a DataFrame
# df = pd.DataFrame(results)

# # Ensure all alternative description columns are present
# for i in range(max_alt_desc_index):
#     if f'alternative desc {i+1}' not in df.columns:
#         df[f'alternative desc {i+1}'] = None

# # Export to CSV
# df.to_csv('diag_data_with_alt_desc.csv', index=False)


# Load the existing CSV file
df = pd.read_csv('diag_data_with_alt_desc.csv')

# Prepare a list to hold the new rows with (code, desc) structure
new_rows = []

# Iterate over the DataFrame
for index, row in df.iterrows():
    code = row['name']  # Assuming 'name' is the column with the code
    main_desc = row['desc']
    # Add the main description row
    new_rows.append({'code': code, 'desc': main_desc})
    
    # Check for each alternative description
    for i in range(1, 21):  # Adjust the range according to the maximum number of alternative descriptions
        alt_desc_key = f'alternative desc {i}'
        if alt_desc_key in row and pd.notnull(row[alt_desc_key]):
            # Add a new row for each non-empty alternative description
            new_rows.append({'code': code, 'desc': row[alt_desc_key]})

# Create a new DataFrame with the new rows
new_df = pd.DataFrame(new_rows)

# Export the new DataFrame to a CSV file
new_df.to_csv('code_desc_pairs.csv', index=False)
