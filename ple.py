
def isICDinNewPLE(subclaim, newPLE, dentalPLE):
    """checks if the icd for a given subclaim is present in our newPLE or dental datasets.

    :param subclaim: the subclaim that needs to be processed
    :type subclaim: api.models.Subclaim

    :param newPLE: This dataset contains mapping between specific ICD10 codes and their corresponding
    procedures (CPTs). This dataset is considered very specific and, thus, aggressive in correlating ICD10
    with CPTs.
    :type newPLE: dict

    :param dentalPLE: this dataset contains maping between dental ICD10 codes and their 
    corresponding dental procedures (CDTs). 
    :type dentalPLE: dict

    :return: True if the subclaim's ICD code is present in one of the two newPLE datasets.
    :rtype: boolean
    """    
    icd = subclaim["ICD CODE"] #still icd10, but can be generic.
    newPleKeys = set(newPLE.keys()) | set(dentalPLE.keys()) #store this somewhere and call it once
    for key in newPleKeys: #trie... prefix datastructure. Look into using a trie.
        if key.startswith(icd):
            return True
    return False


def getStatusNewPLE(subclaim, newPLE, dentalPLE):
    """checks if a procedure (cpt_code) for the provided diagnosis (icd_code) in a subclaim is valid
    given the new databases only. A procedure is considered valid for a specific diagnosis if its 
    relationship is present in our new PLE datasets.

    :param subclaim: the subclaim that needs to be processed
    :type subclaim: api.models.Subclaim

    :param newPLE: This dataset contains mapping between specific ICD10 codes and their corresponding
    procedures (CPTs). This dataset is considered very specific and, thus, aggressive in correlating ICD10
    with CPTs.
    :type newPLE: dict

    :param dentalPLE: this dataset contains maping between dental ICD10 codes and their 
    corresponding dental procedures (CDTs). 
    :type dentalPLE: dict

    :return: True iff the procedure provided in a given subclaim is valid for its corresponding 
    diagnosis.
    :rtype: boolean
    """    
    icd = subclaim["ICD CODE"]
    cpt = subclaim["CPT CODE"]

    for key, cpts in newPLE.items():
        if key.startswith(icd)  and cpt in cpts: #trie...
            return True

    for key, cdts in dentalPLE.items(): #trie...
        if key.startswith(icd) and cpt in cdts:
            return True
    return False


def isICDinOldPLE(subclaim, oldPLE, ICD10index):
    """checks if a procedure (cpt_code) for the provided diagnosis (icd_code) in a subclaim is valid.
    A procedure is considered valid for a specific diagnosis if its relationship is present in our
    PLE datasets.


    :param subclaim: the subclaim that needs to be processed
    :type subclaim: api.models.Subclaim

    :param oldPLE: This dataset contains mapping between ICD9 codes and their corresponding
    procedures (CPTs). This dataset is considered inherintly generic due to the nature of ICD9 codes 
    :type oldPLE: dict
    
    :param ICD10index: the data obtained when converting ICD10 codes to ICD9 codes using GEM.
    :type ICD10index: dict

    :return: True iff the subclaim's icd code is present in the oldPLE dataset.
    :rtype: boolean
    """    
    icd = subclaim["ICD CODE"]
    for icd10 in ICD10index.keys(): 
        if icd10.startswith(icd):##trie
            icd9s = ICD10index[icd10]
            for icd9 in icd9s:
                icd9 = icd9.icd9cm[:3] #transfering from icd10 to icd9 is specific but the database is generic.
                if icd9 in oldPLE:
                    return True
    return False


def getStatusOldPle(subclaim, oldPLE, ICD10index):
    """checks if a procedure (cpt_code) for the provided diagnosis (icd_code) in a subclaim is valid
    given the old database only. A procedure is considered valid for a specific diagnosis if its 
    relationship is present in our old PLE datasets.

    :param subclaim: the subclaim that needs to be processed
    :type subclaim: api.models.Subclaim

    :param oldPLE: This dataset contains mapping between ICD9 codes and their corresponding
    procedures (CPTs). This dataset is considered inherintly generic due to the nature of ICD9 codes 
    :type oldPLE: dict

    :param ICD10index: the data obtained when converting ICD10 codes to ICD9 codes using GEM.
    :type ICD10index: dict

    :return: True iff the procedure provided in a given subclaim is valid for its corresponding 
    diagnosis.
    :rtype: boolean
    """    
    icd = subclaim["ICD CODE"]
    cpt = subclaim["CPT CODE"]
    for icd10, icd9s in ICD10index.items():
        if icd10.startswith(icd): ##trie. 
            for icd9 in icd9s:
                if icd9.icd9cm[:3] in oldPLE and cpt in oldPLE[icd9.icd9cm[:3]]:
                    return True
    return False


def ple(subclaim, datasets):
    """checks if the provided subclaim is valid given our PLE databases. A subclaim is valid iff
    its diagonsis (icd_code) exists in one of our databases (which are oldPLE, newPLE, dentalPLE), 
    and its corresponding procedure (cpt_code) is a plausible procedure for it. 

    :param subclaim: the subclaim that needs to be processed.
    :type subclaim: api.models.Subclaim.

    :param patient_history: a dummy argument that will not be used in this function, defaults to None.
    :type patient_history: a dummy argument that will not be used in this funciion, optional.
    
    :return: (status, error_msgs, violation_ids, causes, hints):
        1. status: 1 iff the ple test passed for the given subclaim and 0 otherwise.
        2. error_msgs: the error messages associated when running the ple test for the provided 
        subclaim. Note that error_msgs = [] if status = 1
        3. violation ids: the ids of the subclaims that caused the violation for the provided
        subclaim, if any.
        4. causes: a list of tuples where each tuple contains the subclaim attributes that correspond
        to an error_msg, if any. 
        5. hints: a list of tuples where each tuple contains the subclaim attributes that correspond
        to the attributes that caused the error. For example, if an error is caused
def ple():
    print("PLE tests complete")
        by <cpt_code>, then <cpt_description> is considered as it provides information about that
        attribute. 
    :rtype: (boolean, List[string], List[string], List[tuple],  List[tuple])
    """

    oldPLE = datasets["oldPLE"]
    newPLE = datasets["newPLE"]
    dentalPLE = datasets["dentalPLE"]
    ICD10index = datasets["ICD10index"]

    ICD_in_oldPLE = isICDinOldPLE(subclaim=subclaim, oldPLE=oldPLE, ICD10index=ICD10index)
    ICD_in_newPLE = isICDinNewPLE(subclaim=subclaim, newPLE=newPLE, dentalPLE=dentalPLE)
    ICD_union_status = ICD_in_newPLE or ICD_in_oldPLE

    newPLE_status = getStatusNewPLE(subclaim=subclaim, newPLE=newPLE, dentalPLE=dentalPLE) 
    oldPLE_status = getStatusOldPle(subclaim=subclaim, oldPLE=oldPLE, ICD10index=ICD10index)
    final_union_status = oldPLE_status or newPLE_status

    status = False
    error_msg = ""

    if not ICD_union_status: ##make this a seperate function.
        error_msg = f"The diagnosis {subclaim['ICD CODE']} was not found in the databases."
    else:
        if not final_union_status:
            error_msg = f" The procedure {subclaim['CPT CODE']} is not a valid a procedure for "
            error_msg += f"the given diagnosis {subclaim['ICD CODE']}"
        else:
            status = True
            error_msg = f"Successfully matched procedure {subclaim['CPT CODE']} to diagnosis {subclaim['ICD CODE']}"
    return (status, error_msg)