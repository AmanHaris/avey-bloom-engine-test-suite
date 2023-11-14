import requests
import json
import pandas as pd
import numpy as np

from avey_nlp_code_translations import nlp_to_avey_code

################################ Make final symptoms file ##########################################


# Assume this is your custom function that takes three arguments and returns a value
def calculate_final_code(nlp_desc, doctor_opinion, code_desc):
    # Your logic to calculate the final code goes here
    # For demonstration, let's just concatenate the strings
    if code_desc:
        print("code desc: ", code_desc)
        res = nlp_to_avey_code(code_desc)
        print(res)
        return res
    if doctor_opinion:
        return ""
    return nlp_to_avey_code(nlp_desc)


# Function to read the CSV, add a column, and save back to CSV
def add_column_to_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, converters={i : str for i in range(0,100)})
    
    # Apply the calculate_final_code function to each row and create the new column
    # The lambda function extracts the relevant columns for each row and passes them to your function
    df['Avey code (final)'] = df.apply(lambda row: calculate_final_code(row['Avey Description (NLP)'], 
                                                                        row["Avey code (Doctor’s opinion)"], 
                                                                        row['Avey code description']), axis=1)
    
    # Write the modified DataFrame back to a new CSV file
    df.to_csv('modified_' + file_path, index=False)

# Replace 'your_file.csv' with the path to your actual CSV file
# add_column_to_csv('essential_symptoms_list_reviewed.csv')

######################## HANDLE REQUESTS ######################################





def produce_diagnoses(sympt_list):

    # The URL of the API endpoint

    url = 'https://localhost:8080/api/v1/ask'



    # The JSON payload you want to send

    data_to_send = {

        "API_SECRET_KEY": "1d57f935-635a-4447-bae5-b645f404fc13",

        "age": 25,

        "chief_findings": [int(x) for x in sympt_list if not np.isnan(x)],

        "cookies": {

        },

        "findings": {

        },

        "image": {

        },

        "next_question": "",

        "question_count": 100,

        "sex": "male"

    }





    # Send a POST request with JSON data

    response = requests.post(url, json=data_to_send, verify=False)



    # Check if the request was successful

    if response.status_code == 200:

        res = []

        # Handle successful response

        diseases = response.json()["diagnosis"]["diseases"]  # The JSON response from the API

        for lst in diseases:

            for entry in lst:

                res.append(("diagnosis (instance)", entry["instances"][0]["instance"], 
                            "multiple instances", str(len(entry["instances"]) > 1),
                            "confidence", entry["instances"][0]["confidence"]["Current"], 
                            "min_confidence", entry["instances"][0]["confidence"]["MinConfidence"], 
                            "confidence_age_seriousness", entry["instances"][0]["confidence_age_seriousness"]))

        print(res)
        return res

    else:

        # Handle request errors
        print('Request failed with status code', response.status_code)
        exit(1)

        #print(response.json())  # This prints the JSON response from the API


####################### PREPARE REQUESTS ######################################

# Function that processes a list of Avey codes and returns a list of outputs
def process_avey_codes(avey_codes_list):
    # Your processing logic here
    # This is a placeholder function that should be replaced with your actual logic
    return produce_diagnoses(avey_codes_list)  # Replace this with the actual list of outputs

# Load file A and file B into DataFrames
df_mapping = pd.read_csv('symptoms_coding_archive/modified_essential_symptoms_list_reviewed.csv')  # File with ICD to Avey code mappings
df_codes = pd.read_csv('only_symptoms_DIG_archive/only_symptoms_DIG_standard.csv')  # File with lists of ICD codes

# Create a dictionary for ICD to Avey code mapping
icd_to_avey = pd.Series(df_mapping['Avey code (final)'].values, index=df_mapping['ICD Code']).to_dict()

# Function to convert ICD list to Avey list using the mapping
def convert_to_avey_list(icd_list):
    icd_list = [entry.split()[0] for entry in icd_list if entry.split()[0][0]=='R']
    # print("icd list: ", icd_list)
    temp = [icd_to_avey.get(icd, 'Unknown') for icd in icd_list]  # 'Unknown' for unmapped codes
    res = []
    for code in temp:
        if str(code) != 'nan' and '@' in code:
            print("@ in code: ", code)
            code = code.split('@')
            res += [float(x) for x in code]
        else:
            res.append(float(code))
    print("res: ", res)
    return res


# Apply the conversion to the ICD code lists in file B
df_codes['Avey code list'] = df_codes['ICD'].apply(lambda x: convert_to_avey_list(x.split(',')))

# Apply the process_avey_codes function to each list of Avey codes
outputs = df_codes['Avey code list'].apply(process_avey_codes)

# Assuming the outputs are lists, we'll convert them into a DataFrame
# and concatenate it with df_codes. We're also handling cases where there are less than 8 outputs.
outputs_df = pd.DataFrame(outputs.tolist(), index=df_codes.index).add_prefix('Output_')

# Fill any missing values if the lists have less than 8 items
outputs_df = outputs_df.reindex(columns=[f'Output_{i}' for i in range(8)], fill_value='')

# Concatenate the outputs DataFrame with the original df_codes
df_codes = pd.concat([df_codes, outputs_df], axis=1)

# Save the updated DataFrame to a new CSV file
df_codes.to_csv('only_symptoms_DIG_new_results.csv', index=False)



