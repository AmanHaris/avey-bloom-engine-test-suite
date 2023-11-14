

# imports
from collections import defaultdict


# changes a list of dict into a dict of lists collected based on a single key
def combineByKey(dict_list, dict_keys):
    res = {}
    for entry in dict_list:
        key_val = ""
        count = 0
        for k in dict_keys:
            try:
                key_val = key_val + " + "*bool(count) + entry[k]
            except:
                raise Exception(f"key {k} not in subclaim")
            count += 1

        if key_val in res:
            res[key_val].append(entry)
        else:
            res[key_val] = [entry]
    return res

# not the most robust of tests but works for now
def isICD10(code):
    if code[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return False
    if len(code) < 3 or len(code) > 10: #should be 7 actually but I'm leaving some flexibility
        return False
    if not code[1].isdigit() or not code[2].isdigit():
        return False
    return True



# helper class for leading icd10 to icd9 GEM
class Conversion():
    '''
    a class used to represent the information provided by GEM when converting icd10
    data to icd9.
    ''' 
    def __init__(self, row):
        """_summary_

        :param row: a row in the GEM file. Note that a row in GEM file contains the following info:
            1. icd10 code: the icd10 code
            2. icd9 code: the corresponding icd9 code
            3. flags: 5 digit code that contains extra information about the mapping.
            4. approximate
            5. noMap
            6. combination
            7. scenario
            8. choiceList
        :type row: dict
        """        
        rowSplit = row.strip().split(',')
        self.icd10cm = rowSplit[0]
        self.icd9cm = rowSplit[1]
        self.flags = rowSplit[2]
        self.approximate = rowSplit[3]
        self.noMap = rowSplit[4]
        self.combination = rowSplit[5]
        self.scenario = rowSplit[6]
        self.choiceList = rowSplit[7]

    def toJson(self):
        """creates a dictionary (json) of the gem information for 1 row.

        :return: a dictionary representating the information present in 1 row of the gem file.
        :rtype: dict
        """        
        return {
            'icd10cm': self.icd10cm,
            'icd9cm': self.icd9cm,
            'flags': self.flags,
            'approximate': self.approximate,
            'noMap': self.noMap,
            'combination': self.combination,
            'scenario': self.scenario,
            'choiceList': self.choiceList,
        }


# helper function for leading icd10 to icd9 GEM
def getICD10index(f):
    """creates GEM dataset from a GEM dataset file.

    :param f: file object corresponding to the GEM dataset file that needs to be processed.
    :type f: io.TextIOWrapper (file pointer) 

    :return: GEM dataset
    :rtype: Dict[string (icd10_code) -> Conversion (dict)]
    """    
    ICD10index = defaultdict(list)
    data = [Conversion(line.replace('"','')) for line in f.readlines()[1:]]
    for item in data:
        ICD10index[item.icd10cm].append(item)
    return ICD10index