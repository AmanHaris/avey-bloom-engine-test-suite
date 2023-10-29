"""

Add any new claim formats into this file

"""


import pandas as pd


# set the path to the directory with claims from root here
claims_location = 'claims/'


# currently supported organizations
claimSetOptions = {'Seib','AlKoot', 'QIC', 'DIG', 'QLM'}


"""
Generic Claims Meta-Data Class
"""
class ClaimInfo:
    def __init__(self, id, files, mappings, group_by):
        self.id = id # string ID of your organization (Seib, AlKoot, ...)
        self.files = files # set of filenames from your organization
        self.mappings = mappings # a dictionary mapping expected column names to available column names in your format
        self.group_by = group_by # a set of columns whose values together uniquely identify a claim from subclaims

    # function that maps organization column names to generic column names
    def regularize(self, subclaims):
        for subclaim in subclaims:
            for k, alt_names in self.mappings.items():
                for v in alt_names:
                    if v in subclaim:
                        subclaim[k] = subclaim[v]
                        if self.id == 'Seib':
                            subclaim[k] = subclaim[v].split()[0]
                        if self.id == 'QIC':
                            subclaim[k] = subclaim[v].split()[-1]

    # function that opens claims file of different specifications
    def openClaimFile(self, filename):
        path = claims_location + filename
        file_extension = filename[filename.rfind('.'):] 

        if file_extension == '.xlsx':
            df = pd.read_excel(path, dtype=str)
        elif file_extension == '.csv':
            df = pd.read_csv(path, dtype=str)
        
        try:
            dict_list = df.to_dict(orient='records')
            return dict_list
        except:
            raise ValueError("Filename given to openClaimFile has an unsupported filetype!")


# Add any tweaks related to Seib here
Seib = ClaimInfo(
    id = 'Seib',
    files = {'ClaimsSeib1.xlsx', 'ClaimsSeib2.xlsx'},
    mappings = {
        "ICD CODE" : {"ICD CODES", "ICD CODE 1"},
        "CPT CODE" : {"CPT CODES"}
    },
    group_by = {'INSURED MEMBER', 'TRX DATE'}
    )


# Add any tweaks related to AlKoot here
AlKoot = ClaimInfo(
    id = 'AlKoot',
    files = {"ClaimsAlKoot1.csv", "ClaimsAlKoot2.csv"},
    mappings = {
        "ICD CODE" : {"PRINCIPAL ICD CODE"},
        "CPT CODE" : {"CPT CODE, SYMPTOMS"}
    },
    group_by = {"SYMPTOMS"}
    )


# Add any tweaks related to QIC here
QIC = ClaimInfo(
    id = 'QIC',
    files = {'ClaimsQIC1.csv', 'ClaimsQIC2.csv', 'ClaimsQIC3.csv', 'ClaimsQIC4.csv'},
    mappings = {
        "ICD CODE" : {"Diagnosis Code", "Diagnosis Name"},
        "CPT CODE" : {"CPT Code", "Provider Service Code", "Provider service Code"}
    },
    group_by = {"Claim No"}
    )


# Add any tweaks related to DIG here
DIG = ClaimInfo(
    id = 'DIG',
    files = {"ClaimsDIG1.csv"},
    mappings = {
        "ICD CODE" : {"Primary Diagnosis ICD 10 code*", },
        "CPT CODE" : {"CPT code*"}
    },
    group_by = {"Member ID*", "Date*"}
    #group_by = {"Claim #*"}
    )


# Add any tweaks related to QLM here
QLM = ClaimInfo(
    id = 'QLM',
    files = {'ClaimsQLM1.csv', 'ClaimsQLM2.csv'},
    mappings = {
        "ICD CODE" : {"Primary Diag Code"},
        "CPT CODE" : {"CPT Code"}
    },
    group_by = {"Invoice No."}
    )


# A function that returns the set of organizations to be tested
# input: claimsetOption shuold be 'ALL' or should be one of the supported organization names
def generateClaimSet(claimsetOption):
    testSet = {Seib, AlKoot, QIC, DIG, QLM}
    if claimsetOption != 'ALL':
        for org in testSet:
            if org.id.lower() == claimsetOption.lower():
                return {org}
    return testSet