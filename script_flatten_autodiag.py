import pandas as pd

def flatten_tuples_in_csv(file_path, output_file):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Number of output columns
    num_output_cols = 8

    # Process each 'Output_i' column
    for i in range(num_output_cols):
        col_name = f'Output_{i}'

        # Create new columns based on the first row (assuming consistency in tuple structure)
        first_row_tuple_str = df.at[0, col_name].strip('()')  # Remove parentheses
        first_row_tuple_elements = first_row_tuple_str.split(', ')  # Split elements

        # Extract and create new column names
        for j in range(0, len(first_row_tuple_elements), 2):
            new_col_name = first_row_tuple_elements[j].strip('\'\"') + f' {i+1}'
            df[new_col_name] = None

        # Assign values to new columns
        for index, row in df.iterrows():
            if row[col_name] == None:
                continue
            tuple_str = row[col_name].strip('()')
            tuple_elements = tuple_str.split(', ')

            for j in range(0, len(tuple_elements), 2):
                col_name = tuple_elements[j].strip('\'\"') + f' {i+1}'
                value = tuple_elements[j+1].strip('\'\"')
                df.at[index, col_name] = value

        # Drop the original 'Output_i' column
        df.drop(columns=[col_name], inplace=True)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

flatten_tuples_in_csv('only_symptoms_DIG_new_results.csv', 'flattened_output.csv')
