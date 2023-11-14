import pandas as pd

# Load the CSV file
file_path = 'only_symptoms_DIG_standard.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Check for non-empty entries in the "Any reasonable diagnoses? (Pick 1-8)" column
df['Diagnosis Non-Empty'] = df['Any reasonable diagnoses? (Pick 1-8)'].notna()

# Group by 'ICD count' and count non-empty diagnoses
diagnosis_counts = df.groupby('ICD count')['Diagnosis Non-Empty'].sum()

# Convert the Series to a DataFrame for better formatting
diagnosis_counts_df = diagnosis_counts.reset_index()

# Rename the columns for clarity
diagnosis_counts_df.columns = ['ICD count', 'Non-Empty Diagnosis Count']

# Print the DataFrame
print(diagnosis_counts_df)
