# Import the necessary libraries
import pandas as pd

# Read in the CSV file
df = pd.read_csv('avey-NLP/ICD10_labeled_from_claims.csv')

# Filter out unwanted columns
columns_to_keep = ['ICD CODE', 'DESCRIPTION'] 
df = df[columns_to_keep]

# Define the filter column and valid filters
filter_column = 'ICD CODE'
valid_filters = [
    'R509',             
    'R53',             
    'R51',            
    'R060',             
    'R12',          
    'R634',             
    'R631',             
    'R000',             
    'R224',
    'R040'
]             
# Filter the dataframe by the valid filters in the filter column
df = df[df[filter_column].isin(valid_filters)]

# convert df to a python dictionary for further processing
# d = df.to_dict(orient='records')
# lst = []
# print(type(d))
# for elem in d:
#     vals = columns_to_keep[1:]
#     for val in vals:
#         if str(elem[val] != 'nan'):
#             lst.append((elem['Input.LABEL'], elem[val]))
# print(len(lst))
# lst = list(set(lst))
# print(len(lst))

# lst = [(a, b) for (a, b) in lst if str(a) != 'nan' and str(b) != 'nan']

# # save the list of tuples to a new CSV file
# df = pd.DataFrame(lst, columns=['label', 'text'])
# df.to_csv('avey-NLP/samples/mturk_filtered.csv', index=False)
# #print(lst)


# save the filtered dataframe to a new CSV file
df.to_csv('avey-NLP/samples/ICD10_labeled_from_claims_filtered.csv', index=False)
