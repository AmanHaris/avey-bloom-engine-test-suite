
import os
import json
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import functools
import argparse


# local imports
from ple import ple
from mue import mue
from ppv import ppv
from claims import generateClaimSet, claimSetOptions
import claim_utils


# setups
tqdm.pandas()


# globals:
claimset_option = 'ALL'
functions_option = 'ALL'
functions_options = {'PLE', 'MUE', 'PPV'}


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str)
    parser.add_argument('-f', type=str)
    parser.add_argument('--sampling', type=str)
    args = parser.parse_args()

    if args.c in claimSetOptions:
        claimset_option = args.c
    test_set = generateClaimSet(claimset_option)

    if args.f in functions_options:
        functions_option = args.f

    print(f"Testing for {functions_option} in {claimset_option} claimset")

    for org in test_set:
        print(f"\nRunning tests for {org.id}...")
        for f in org.files:
            print(f"\nTest for file {f}...\n")
            dict_list = org.openClaimFile(f)
            org.regularize(dict_list)
            claimsDict = claim_utils.combineByKey(dict_list, org.group_by)

            print("Total Subclaims: ", len(dict_list))
            print("Total Claims: ", len(claimsDict))

            def __combine_icd_and_cpt(lst):
                ICDs = []
                CPTs = []
                for entry in lst:
                    ICDs.append(entry['ICD CODE'])
                    CPTs.append(entry['CPT CODE'])
                return {"ICD" : ICDs, "CPT" : CPTs}
                

            icd_cpt_list = [ {**__combine_icd_and_cpt(v), **{'ID':k}} for k,v in claimsDict.items()]

            def __only_symptoms(icd_cpt_entry):
                for code in icd_cpt_entry['ICD']:
                    if code[0] != 'R':
                        return False
                return True

            only_symptoms_list = [entry for entry in icd_cpt_list if __only_symptoms(entry)]
            # print(onlySymptomsList)
            print("Total instances of only symptoms in claim: ", len(only_symptoms_list))


            ### Separating out claims with only valid CPT codes

            claims_good_CPT = filter(icd_cpt_list)
            only_symptoms_good_CPT = filter(only_symptoms_list)



        # run PLE
        if functions_option in {'ALL', 'PLE'}:
            ple() # placeholder

        if functions_option in {'ALL', 'MUE'}:
            mue() # placeholder

        if functions_option in {'ALL', 'PPV'}:
            ppv() # placeholder

        # save files
            # version = date + time
            # mkdir for version
            # store results in versioned dir

