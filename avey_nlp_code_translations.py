import pandas as pd


def nlp_to_avey_code(description):
    description = description.lower()
    location = "algorithm-datasets/"
    files = ["searchables.csv", "non-searchables.csv"]

    for file in files:
        df = pd.read_csv(location + file, converters={i: str for i in range(0, 100)})

        name_id_list = list(zip((df["name"]), df["id"]))
        
        name_id_list_lower = [ (a.lower(), b) for (a, b) in name_id_list] 
        name_id_dict = dict(name_id_list_lower)
        if description in name_id_dict:
            return name_id_dict[description]


# Read the CSV file into a DataFrame
# df = pd.read_csv("essential_symptoms_list.csv", converters={i: str for i in range(0, 100)})

# # Apply the function to the 'code' column based on the 'description' column
# df['Code in NLP engine (NLP)'] = df.apply(lambda row: nlp_to_avey_code(row['Avey Description (NLP)']), axis=1)

# # If you wish to save the modified DataFrame back to a CSV:
# df.to_csv("essential_symptoms_list_updated.csv", index=False)
