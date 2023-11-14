
import os
import json
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import functools
import argparse
import copy


# local imports
from ple import ple
from mue import mue
from ppv import ppv
from claims import generateClaimSet, claimSetOptions, SECONDARY_ICD_LIMIT
import claim_utils


# setups
tqdm.pandas()


# globals:
claimset_option = 'ALL'
functions_option = 'ALL'
functions_options = {'PLE', 'MUE', 'PPV'}


# file locations
PLE_DATABASE_DIR = 'algorithm-datasets/PLE_databases/'
DENTAL_PLE = PLE_DATABASE_DIR + 'icdTocdt.json'
OLD_PLE = PLE_DATABASE_DIR + 'oldPLE.json'
NEW_PLE = PLE_DATABASE_DIR + 'icdTocpt.json'
ICD10_TO_ICD9 = 'algorithm-datasets/icd10toicd9/icd10cmtoicd9gem.csv'


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

    # Load Datasets

    Datasets = {}
    (f1, f2, f3, f4) = (open(OLD_PLE, 'r'), open(NEW_PLE, 'r'),
                        open(DENTAL_PLE, 'r'), open(ICD10_TO_ICD9, 'r'))
    Datasets["oldPLE"] = json.load(f1)
    Datasets["newPLE"] = json.load(f2)
    Datasets["dentalPLE"] = json.load(f3)
    Datasets["ICD10index"] = claim_utils.getICD10index(f4)

    print(f"Testing for {functions_option} in {claimset_option} claimset")

    ICD10_mappings = {}

    for org in test_set:
        print(f"\nRunning tests for {org.id}...")
        for f in org.files:
            print(f"\nTest for file {f}...\n")
            dict_list = org.openClaimFile(f)
            org.regularize(dict_list)

            for subclaim in dict_list:
                if subclaim["ICD CODE"] not in ICD10_mappings:
                    ICD10_mappings[subclaim["ICD CODE"]] = []
                ICD10_mappings[subclaim["ICD CODE"]].append(subclaim["ICD CODE DESCRIPTION"])

                for i in range(0, SECONDARY_ICD_LIMIT):
                    if subclaim[f"SECONDARY ICD CODE {i+1}"] not in ICD10_mappings:
                        ICD10_mappings[subclaim[f"SECONDARY ICD CODE {i+1}"]] = []
                    ICD10_mappings[subclaim[f"SECONDARY ICD CODE {i+1}"]].append(subclaim[f"SECONDARY ICD CODE {i+1} DESCRIPTION"])

            continue #temporary

            claimsDict = claim_utils.combineByKey(dict_list, org.group_by)

            print("Total Subclaims: ", len(dict_list))
            print("Total Claims: ", len(claimsDict))

            def __combine_icd_and_cpt(lst):
                ICDs = []
                CPTs = []
                ICD_desc = []
                CPT_desc = []
                for entry in lst:
                    CPTs.append(entry['CPT CODE'] + " " + entry['CPT Description'])
                    ICDs.append(entry['ICD CODE'] + " " + entry['Primary Diagnosis ICD 10 description '])
                    for i in range(SECONDARY_ICD_LIMIT):
                        code = entry['SECONDARY ICD CODE '+str(i+1)]
                        if code != "":
                            try:
                                ICDs.append(code + " " + entry[f"Secondary Diagnosis {str(i+1)} - ICD 10 code description "])
                            except:
                                print(f"Secondary Diagnosis {str(i+1)} - ICD 10 code description ")
                                print(entry.keys())
                                exit(1)
                return {"ICD" : ICDs, "CPT" : CPTs}
                

            icd_cpt_list = [ {**__combine_icd_and_cpt(v), **{'ID':k}} for k,v in claimsDict.items()]

            def __only_symptoms(icd_cpt_entry):
                for code in icd_cpt_entry['ICD']:
                    if code[0] != 'R':
                        return False
                # print(icd_cpt_entry["ID"], icd_cpt_entry['ICD'])
                return True

            only_symptoms_list = [entry for entry in icd_cpt_list if __only_symptoms(entry)]
            # print(onlySymptomsList)
            print("Total instances of only symptoms in claim: ", len(only_symptoms_list))


            ### Separating out claims with only valid CPT codes

            global_cpts1 =  set().union(*[set(v) for v in Datasets['newPLE'].values()])
            global_cpts2 = set().union(*[set(v) for v in Datasets['dentalPLE'].values()])
            global_cpts3 = set().union(*[set(v) for v in Datasets['oldPLE'].values()])
            global_cpts = global_cpts1.union(global_cpts2.union(global_cpts3))
            print("total nCPT count = ", len(global_cpts1))
            print("total CDT count = ", len(global_cpts2))
            print("total oCPT count = ", len(global_cpts3))
            print("total count = ", len(global_cpts))

            def __cpt_code_check(code):
                if len(code) != 5:
                    return False
                if code[0] not in "0123456789D":
                    return False
                if code[1] not in "0123456789":
                    return False
                if code[2] not in "0123456789":
                    return False
                if code[3] not in "0123456789":
                    return False
                if code[4] not in "0123456789U":
                    return False
                return True
                

            def __has_cpt(subclaim):
                CPTs = subclaim['CPT']
                res = True
                for code in CPTs:
                    res = res and (code in global_cpts or __cpt_code_check(code))
                #if (res == False): print(CPTs)
                return res

            claims_good_CPT = list(filter(__has_cpt, icd_cpt_list))
            only_symptoms_good_CPT = list(filter(__has_cpt, only_symptoms_list))

            print("")


        # run PLE
            if functions_option in {'ALL', 'PLE'}:
                # for claims with diagnosis:
                print("\n running PLE tests... \n")
                print("\n total claims with a valid CPT code: ", len(claims_good_CPT) + len(only_symptoms_good_CPT))
                print("\n total claims with a valid CPT code and good primary diagnosis: ", len(claims_good_CPT))
                print("\n total claims with a valid CPT code and a symptom as primary diagnosis: ", len(only_symptoms_good_CPT))
                hits = 0
                for claim in claims_good_CPT:
                    principal_icd_code = claim['ICD'][0]
                    cpt_codes = claim['CPT']
                    passed = True
                    for code in cpt_codes:
                        subclaim = copy.deepcopy(claim)
                        subclaim['ICD CODE'] = principal_icd_code
                        subclaim['CPT CODE'] = code
                        (status, msg) = ple(subclaim, Datasets)
                        # print(status, msg)
                        passed = passed and status
                    if passed:
                        hits += 1
                print("\n total claims passed with primary diagnosis = ", hits)

                hits = 0
                for claim in only_symptoms_good_CPT:
                    principal_icd_code = claim['ICD'][0]
                    cpt_codes = claim['CPT']
                    passed = True
                    for code in cpt_codes:
                        subclaim = copy.deepcopy(claim)
                        subclaim['ICD CODE'] = principal_icd_code
                        subclaim['CPT CODE'] = code
                        (status, msg) = ple(subclaim, Datasets)
                        # print(status, msg)
                        passed = passed and status
                    if passed:
                        hits += 1
                print("\n total claims passed with only symptom= ", hits)

                unique_symptoms = set()
                for claim in only_symptoms_list:
                    claim['ICD count'] = len(set(claim['ICD']))
                    unique_symptoms = unique_symptoms.union(set(claim['ICD']))

                    claim['ICD'] = ", ".join(set(claim['ICD']))
                    claim['CPT'] = ", ".join(set(claim['CPT']))
                    # if claim['ICD count'] > 3:
                    #     print(claim['ICD count'], claim['ICD'])



                #print(len(unique_symptoms), unique_symptoms)
                
                # df = pd.read_json(json.dumps(only_symptoms_list))
                # df.to_csv("only_symptoms_DIG.csv")

                unique_tuples = []
                for code in unique_symptoms:
                    idx = code.find(" ")
                    unique_tuples.append((code[:idx], code[idx+1:]))
                    #print(f"(\"{code[:idx]}\", \"{code[idx+1:]}\"),")                

                df2 = pd.DataFrame(unique_tuples, columns=["ICD Code", "ICD Description", "Code in NLP engine (NLP)", "Avey Description (NLP)"])
                df2.to_csv("essential_symptoms_list.csv", index=False)

            if functions_option in {'ALL', 'MUE'}:
                mue() # placeholder

            if functions_option in {'ALL', 'PPV'}:
                ppv() # placeholder

            # save files
                # version = date + time
                # mkdir for version
                # store results in versioned dir

def regularize_ICD(s):
    res = []
    for c in s:
        if c!=" " and c!= ",":
            res.append(c.upper())
    return "".join(res)

# Convert the dictionary into a list of tuples
data_tuples = [(regularize_ICD(key), value) for key, values in ICD10_mappings.items() for value in values if value and claim_utils.isICD10(key)]

#data_tuples.sort(key = lambda x : len(x[1]))

# case sensitive
final_dict = {k : [] for (k, v) in data_tuples}
for (k, v) in data_tuples:
    final_dict[k].append(v)

print("case sensitive: ")
print(f"Total pairs, codes, desc per code = {len(data_tuples)}, {len(final_dict.keys())}, {len(data_tuples) / len(final_dict.keys())}")

res = list(map(lambda x : (x[0], len(x[1])), list(final_dict.items())))
res2 = list(map(lambda x : (x[0], set([s.lower() for s in x[1]])), list(final_dict.items())))

res.sort(key=lambda x : x[1], reverse=True)
res2.sort(key=lambda x : len(x[1]), reverse=True)

res2 = {k : v for (k, v) in res2}

for i in range(100):
    print(res[i], res2[res[i][0]])

print("\n Now printing top symptoms... \n")

res3 = [(s, c, res2[s]) for (s,c) in res if s[0] == 'R']
res3 = res3[:100]
for elem in res3:
    print(elem)

exit(0)

# case insensitive
final_dict = {k : set() for (k, v) in data_tuples}
for (k, v) in data_tuples:
    final_dict[k].add(v.lower())

data_tuples = [(key, value) for key, values in final_dict.items() for value in values if value and claim_utils.isICD10(key)]

print("case insensitive: ")
print(f"Total pairs, codes, desc per code = {len(data_tuples)}, {len(final_dict.keys())}, {len(data_tuples) / len(final_dict.keys())}")

# Create a DataFrame
df = pd.DataFrame(data_tuples, columns=['ICD CODE', 'DESCRIPTION'])

# Save the DataFrame to a CSV file
df.to_csv('ICD10_mappings.csv', index=False)


