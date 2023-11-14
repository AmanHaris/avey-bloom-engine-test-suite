import pandas as pd

def remove_empty_columns(file_path, output_file):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Remove columns where all values are NaN
    df.dropna(axis=1, how='all', inplace=True)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# Example usage
remove_empty_columns('flattened_output.csv', 'only_symptoms_DIG_instances.csv')
