
import pandas as pd
import numpy as np

# Load the master.csv file
df = pd.read_csv("avey-NLP/samples/master.csv")

# Get unique labels and generate indices for them
unique_labels = df['label'].unique()
label2ind = {label: index for index, label in enumerate(unique_labels)}
ind2label = {index: label for index, label in enumerate(unique_labels)}

# Save label2ind and ind2label as csv files
label2ind_df = pd.DataFrame.from_dict(label2ind, orient='index', columns=['index'])
label2ind_df.index.name = 'label'
label2ind_df.to_csv('avey-NLP/samples/label2ind.csv')

ind2label_df = pd.DataFrame.from_dict(ind2label, orient='index', columns=['label'])
ind2label_df.index.name = 'index'
ind2label_df.to_csv('avey-NLP/samples/ind2label.csv')

# Save the updated master.csv file with indices for labels
df['label'] = df['label'].apply(lambda x: label2ind[x])
df.to_csv('avey-NLP/samples/master_with_indices.csv', index=False)

# open test_set.csv and validation_set.csv, convert their labels to indices, and save them
test_set = pd.read_csv('avey-NLP/samples/test_set.csv')
test_set['label'] = test_set['label'].apply(lambda x: label2ind[x])
test_set.to_csv('avey-NLP/samples/test_set_with_indices.csv', index=False)

validation_set = pd.read_csv('avey-NLP/samples/validation_set.csv')
validation_set['label'] = validation_set['label'].apply(lambda x: label2ind[x])
validation_set.to_csv('avey-NLP/samples/validation_set_with_indices.csv', index=False)


