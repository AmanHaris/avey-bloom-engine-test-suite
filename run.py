
import os
import json
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import functools

# local imports
from ple import ple
from mue import mue
from ppv import ppv
import claim_utils

# setups
tqdm.pandas()

# globals:

claims_location = 'claims/'
# claims_seib = 'ClaimsSeib2.xlsx' TODO: accommodating multiple claim files and claim types per organization
claims_seib = 'ClaimsSeib1.xlsx'
claims_qic = 'ClaimsQIC.csv'
claims_alkoot = None
test_set = set(['Seib', 'QIC', 'AlKoot'])

claimset_option = 'Seib' # placeholder until I add getopt

# load files
claims = {'Seib' : claims_seib, 'QIC' : claims_qic, 'AlKoot' : claims_alkoot}

if claimset_option != 'ALL':
    test_set = [claimset_option]
    claims = {claimset_option : claims[claimset_option]}


#df_qic = pd.read_csv(claims_location + claims_qic, dtype=str, index_col=0)

# TODO: at the moment, this implementation is specific to Seib, need to generalize
for org in test_set:

    df = pd.read_excel(claims_location + claims[org], dtype=str) # TODO: excel/csv depends on org
    dict_list = df.to_dict(orient='records')

    # TODO: need to standardize claim column names before getting to  any code below here

    claimsDict = claim_utils.combineByKey(dict_list, 'CLAIM NUMBER')
    # claimsDict = claim_utils.combineByKey(dict_list, 'INSURED MEMBER', 'TRX DATE')
    print("Total Subclaims: ", len(dict_list))
    print("Total Claims: ", len(claimsDict))

    def __combine_icd_and_cpt(lst):
        ICDs = []
        CPTs = []
        for entry in lst:
            ICDs.append(entry['ICD CODES'].split()[0])
            CPTs.append(entry['CPT CODES'])
        return {"ICD" : ICDs, "CPT" : CPTs}
        

    icd_cpt_list = [ {**__combine_icd_and_cpt(v), **{'ID':k}} for k,v in claimsDict.items()]

    def __onlySymptoms(icd_cpt_entry):
        for code in icd_cpt_entry['ICD']:
            if code[0] != 'R':
                return False
        return True

    onlySymptomsList = [entry for entry in icd_cpt_list if __onlySymptoms(entry)]
    # print(onlySymptomsList)
    print("Total instances of only symptoms in claim: ", len(onlySymptomsList))



# run PLE
ple() # placeholder

# run MUE
mue() # placeholder

# run TPM
ppv() # placeholder

# save files

    # version = date + time
    # mkdir for version
    # store results in versioned dir

