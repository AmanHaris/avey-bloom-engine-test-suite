import pandas as pd
import random

# Load the csv files
df1 = pd.read_csv('avey-NLP/samples/chatGPT_filtered.csv')
df2 = pd.read_csv('avey-NLP/samples/ICD10_from_claims_filtered.csv')
df3 = pd.read_csv('avey-NLP/samples/mturk_filtered.csv')
df4 = pd.read_csv('avey-NLP/samples/manual_filtered.csv')

# Combine the dataframes
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# save df into a master csv file
df.to_csv('avey-NLP/samples/master.csv', index=False)

# Shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)

# Split into test and validation sets
test_size = int(len(df) * 0.9)
test_set = df[:test_size]
validation_set = df[test_size:]

# Save the sets to csv files
test_set.to_csv('avey-NLP/samples/test_set.csv', index=False)
validation_set.to_csv('avey-NLP/samples/validation_set.csv', index=False)
