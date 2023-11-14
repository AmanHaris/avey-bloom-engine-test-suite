import pandas as pd

# Load the CSV file
file_path = 'code_desc_pairs.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Create a mapping from 'code' to index
unique_codes = df['code'].unique()
code2index = {code: idx for idx, code in enumerate(unique_codes)}

# Create a mapping from index to 'code'
index2code = {idx: code for code, idx in code2index.items()}

# Map the 'code' to its corresponding index
df['label'] = df['code'].map(code2index)

# Save the new CSV file with 'code index' and 'desc'
new_file_path = 'ICD_descriptions_and_labels.csv'  # Replace with your desired new CSV file path
df[['label', 'desc']].to_csv(new_file_path, index=False)

# Save the code2index and index2code mappings
code2index_file = 'code2index.csv'  # Replace with your desired file path
index2code_file = 'index2code.csv'  # Replace with your desired file path

# Convert the mappings to DataFrames
code2index_df = pd.DataFrame(list(code2index.items()), columns=['code', 'index'])
index2code_df = pd.DataFrame(list(index2code.items()), columns=['index', 'code'])

# Save the mappings to CSV
code2index_df.to_csv(code2index_file, index=False)
index2code_df.to_csv(index2code_file, index=False)

print("CSV file with code index saved as:", new_file_path)
print("code2index mapping saved as:", code2index_file)
print("index2code mapping saved as:", index2code_file)
