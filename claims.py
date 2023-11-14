"""
*
* Add any new claims into this file
*
"""


import pandas as pd


# set the path to the directory with claims from root here
claims_location = 'claims/'


# currently supported organizations
claimSetOptions = {'Seib','AlKoot', 'QIC', 'DIG', 'QLM'}

# theoretically unbounded, we are enforcing for engineering reasons
SECONDARY_ICD_LIMIT = 13


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
                found = False
                for v in alt_names:
                    if v in subclaim:
                        found = True
                        subclaim[k] = subclaim[v]
                        # Seib
                        if self.id == 'Seib' and k == "ICD CODE":
                            icdList = subclaim[v].split("@")
                            subclaim["ICD CODE"] = icdList[0].split(" ", 1)[0]
                            if len(icdList[0].split()) > 1:
                                subclaim["ICD CODE DESCRIPTION"] = icdList[0].split(" ", 1)[1]
                            for i in range(1, len(icdList)):
                                subclaim["SECONDARY ICD CODE "+str(i)] = icdList[i].split(" ", 1)[0]
                                subclaim[f"SECONDARY ICD CODE {str(i)} DESCRIPTION"] = icdList[i].split(" ", 1)[1]

                        # QIC
                        if self.id == 'QIC':
                            if k == "ICD CODE":
                                subclaim["ICD CODE"] = subclaim[v].split()[-1]
                                subclaim["ICD CODE DESCRIPTION"] = subclaim[v][:subclaim[v].rfind(" ")-2]

                        # DIG
                        if self.id == 'DIG':
                            if "DESCRIPTION" in k:
                                test = subclaim[k].split(" ", 2)
                                if '.' in test[0] and test[0][1] in "0123456789":
                                    subclaim[k] = test[1]

                if not found and k not in subclaim:
                    subclaim[k] = ""
            
            subclaim['ICD CODE'] = subclaim['ICD CODE'].replace(".", "")
            for i in range(SECONDARY_ICD_LIMIT):
                try:
                    subclaim['SECONDARY ICD CODE '+str(i+1)] = subclaim['SECONDARY ICD CODE '+str(i+1)].replace(".", "")
                except:
                    print(subclaim)
                    subclaim['SECONDARY ICD CODE '+str(i+1)] = subclaim['SECONDARY ICD CODE '+str(i+1)].replace(".", "")

    # function that opens claims file of different specifications
    def openClaimFile(self, filename):
        path = claims_location + filename
        file_extension = filename[filename.rfind('.'):] 

        if file_extension == '.xlsx':
            df = pd.read_excel(path, converters={i: str for i in range(0, 100)})
        elif file_extension == '.csv':
            df = pd.read_csv(path, converters={i: str for i in range(0, 100)})
        
        try:
            dict_list = df.to_dict(orient='records')
            return dict_list
        except:
            raise ValueError("Filename given to openClaimFile has an unsupported filetype!")


# Add any tweaks related to Seib here
Seib = ClaimInfo(
    id = 'Seib',
    files = {'ClaimsSeib1.csv', 'ClaimsSeib2.csv'},
    mappings = {
        "ICD CODE" : {"ICD CODES", "ICD CODE 1"},
        "ICD CODE DESCRIPTION" : {"ICD DESC 1"}, # handle Seib as special case for '@' joined codes (see ClaimsSeib1.xlsx)
        "CPT CODE" : {"CPT CODES"},
        "SECONDARY ICD CODE 1": {"ICD CODE 2"},
        "SECONDARY ICD CODE 2": {"ICD CODE 3"},
        "SECONDARY ICD CODE 3": {"ICD CODE 4"},
        "SECONDARY ICD CODE 4": {"ICD CODE 5"},
        "SECONDARY ICD CODE 5": {"ICD CODE 6"},
        "SECONDARY ICD CODE 6": {"ICD CODE 7"},
        "SECONDARY ICD CODE 7": {"ICD CODE 8"},
        "SECONDARY ICD CODE 8": {"ICD CODE 9"},
        "SECONDARY ICD CODE 9": {"ICD CODE 10"},
        "SECONDARY ICD CODE 10": {"ICD CODE 11"},
        "SECONDARY ICD CODE 11": {"ICD CODE 12"},
        "SECONDARY ICD CODE 12": {"ICD CODE 13"},
        "SECONDARY ICD CODE 13": {"ICD CODE 14"},
        "SECONDARY ICD CODE 1 DESCRIPTION": {"ICD DESC 2"},
        "SECONDARY ICD CODE 2 DESCRIPTION": {"ICD DESC 3"},
        "SECONDARY ICD CODE 3 DESCRIPTION": {"ICD DESC 4"},
        "SECONDARY ICD CODE 4 DESCRIPTION": {"ICD DESC 5"},
        "SECONDARY ICD CODE 5 DESCRIPTION": {"ICD DESC 6"},
        "SECONDARY ICD CODE 6 DESCRIPTION": {"ICD DESC 7"},
        "SECONDARY ICD CODE 7 DESCRIPTION": {"ICD DESC 8"},
        "SECONDARY ICD CODE 8 DESCRIPTION": {"ICD DESC 9"},
        "SECONDARY ICD CODE 9 DESCRIPTION": {"ICD DESC 10"},
        "SECONDARY ICD CODE 10 DESCRIPTION": {"ICD DESC 11"},
        "SECONDARY ICD CODE 11 DESCRIPTION": {"ICD DESC 12"},
        "SECONDARY ICD CODE 12 DESCRIPTION": {"ICD DESC 13"},
        "SECONDARY ICD CODE 13 DESCRIPTION": {"ICD DESC 14"},
    },
    group_by = {'INSURED MEMBER', 'TRX DATE'}
    )


# Add any tweaks related to AlKoot here
AlKoot = ClaimInfo(
    id = 'AlKoot',
    files = {"ClaimsAlKoot1.csv", "ClaimsAlKoot2.csv"},
    mappings = {
        "ICD CODE" : {"PRINCIPAL ICD CODE"},
        "ICD CODE DESCRIPTION" : {"ICD DESCRIPTION"},
        "CPT CODE" : {"CPT CODE, SYMPTOMS"},
        "SECONDARY ICD CODE 1": {"SECONDARY ICD CODE 1"},
        "SECONDARY ICD CODE 2": {"SECONDARY ICD CODE 2"},
        "SECONDARY ICD CODE 3": {"SECONDARY ICD CODE 3"},
        "SECONDARY ICD CODE 4": {"SECONDARY ICD CODE 4"},
        "SECONDARY ICD CODE 5": {"SECONDARY ICD CODE 5"},
        "SECONDARY ICD CODE 6": {},
        "SECONDARY ICD CODE 7": {},
        "SECONDARY ICD CODE 8": {},
        "SECONDARY ICD CODE 9": {},
        "SECONDARY ICD CODE 10": {},
        "SECONDARY ICD CODE 11": {},
        "SECONDARY ICD CODE 12": {},
        "SECONDARY ICD CODE 13": {},
        "SECONDARY ICD CODE 1 DESCRIPTION": {},
        "SECONDARY ICD CODE 2 DESCRIPTION": {},
        "SECONDARY ICD CODE 3 DESCRIPTION": {},
        "SECONDARY ICD CODE 4 DESCRIPTION": {},
        "SECONDARY ICD CODE 5 DESCRIPTION": {},
        "SECONDARY ICD CODE 6 DESCRIPTION": {},
        "SECONDARY ICD CODE 7 DESCRIPTION": {},
        "SECONDARY ICD CODE 8 DESCRIPTION": {},
        "SECONDARY ICD CODE 9 DESCRIPTION": {},
        "SECONDARY ICD CODE 10 DESCRIPTION": {},
        "SECONDARY ICD CODE 11 DESCRIPTION": {},
        "SECONDARY ICD CODE 12 DESCRIPTION": {},
        "SECONDARY ICD CODE 13 DESCRIPTION": {},
    },
    group_by = {"SYMPTOMS", "PRINCIPAL ICD CODE"}
    )


# Add any tweaks related to QIC here
QIC = ClaimInfo(
    id = 'QIC',
    files = {'ClaimsQIC1.csv', 'ClaimsQIC2.csv', 'ClaimsQIC3.csv', 'ClaimsQIC4.csv'},#, 'ClaimsQIC2.csv', 'ClaimsQIC3.csv', 'ClaimsQIC4.csv'},
    mappings = {
        "ICD CODE" : {"Diagnosis Name"},
        "ICD CODE DESCRIPTION" : {}, # populated as special case of "ICD CODE" 
        "CPT CODE" : {"CPT Code", "Provider Service Code", "Provider service Code"},
        "SECONDARY ICD CODE 1": {},
        "SECONDARY ICD CODE 2": {},
        "SECONDARY ICD CODE 3": {},
        "SECONDARY ICD CODE 4": {},
        "SECONDARY ICD CODE 5": {},
        "SECONDARY ICD CODE 6": {},
        "SECONDARY ICD CODE 7": {},
        "SECONDARY ICD CODE 8": {},
        "SECONDARY ICD CODE 9": {},
        "SECONDARY ICD CODE 10": {},
        "SECONDARY ICD CODE 11": {},
        "SECONDARY ICD CODE 12": {},
        "SECONDARY ICD CODE 13": {},
        "SECONDARY ICD CODE 1 DESCRIPTION": {},
        "SECONDARY ICD CODE 2 DESCRIPTION": {},
        "SECONDARY ICD CODE 3 DESCRIPTION": {},
        "SECONDARY ICD CODE 4 DESCRIPTION": {},
        "SECONDARY ICD CODE 5 DESCRIPTION": {},
        "SECONDARY ICD CODE 6 DESCRIPTION": {},
        "SECONDARY ICD CODE 7 DESCRIPTION": {},
        "SECONDARY ICD CODE 8 DESCRIPTION": {},
        "SECONDARY ICD CODE 9 DESCRIPTION": {},
        "SECONDARY ICD CODE 10 DESCRIPTION": {},
        "SECONDARY ICD CODE 11 DESCRIPTION": {},
        "SECONDARY ICD CODE 12 DESCRIPTION": {},
        "SECONDARY ICD CODE 13 DESCRIPTION": {},
    },
    group_by = {"Claim No"}
    )


# Add any tweaks related to DIG here
DIG = ClaimInfo(
    id = 'DIG',
    files = {"ClaimsDIG1.csv", "ClaimsDIG2.csv"},
    mappings = {
        "ICD CODE" : {"Primary Diagnosis ICD 10 code*", },
        "ICD CODE DESCRIPTION" : {"Primary Diagnosis ICD 10 description "},
        "CPT CODE" : {"CPT code*"},
        "SECONDARY ICD CODE 1": {"Secondary Diagnosis 1 - ICD 10 code"},
        "SECONDARY ICD CODE 2": {"Secondary Diagnosis 2 - ICD 10 code"},
        "SECONDARY ICD CODE 3": {"Secondary Diagnosis 3 - ICD 10 code"},
        "SECONDARY ICD CODE 4": {"Secondary Diagnosis 4 - ICD 10 code"},
        "SECONDARY ICD CODE 5": {"Secondary Diagnosis 5 - ICD 10 code"},
        "SECONDARY ICD CODE 6": {"Secondary Diagnosis 6 - ICD 10 code"},
        "SECONDARY ICD CODE 7": {"Secondary Diagnosis 7 - ICD 10 code"},
        "SECONDARY ICD CODE 8": {"Secondary Diagnosis 8 - ICD 10 code"},
        "SECONDARY ICD CODE 9": {"Secondary Diagnosis 9 - ICD 10 code"},
        "SECONDARY ICD CODE 10": {"Secondary Diagnosis 10 - ICD 10 code"},
        "SECONDARY ICD CODE 11": {"Secondary Diagnosis 11 - ICD 10 code"},
        "SECONDARY ICD CODE 12": {"Secondary Diagnosis 12 - ICD 10 code"},
        "SECONDARY ICD CODE 13": {"Secondary Diagnosis 13 - ICD 10 code"},
        "SECONDARY ICD CODE 1 DESCRIPTION": {"Secondary Diagnosis 1 - ICD 10 code description "},
        "SECONDARY ICD CODE 2 DESCRIPTION": {"Secondary Diagnosis 2 - ICD 10 code description "},
        "SECONDARY ICD CODE 3 DESCRIPTION": {"Secondary Diagnosis 3 - ICD 10 code description "},
        "SECONDARY ICD CODE 4 DESCRIPTION": {"Secondary Diagnosis 4 - ICD 10 code description "},
        "SECONDARY ICD CODE 5 DESCRIPTION": {"Secondary Diagnosis 5 - ICD 10 code description "},
        "SECONDARY ICD CODE 6 DESCRIPTION": {"Secondary Diagnosis 6 - ICD 10 code description "},
        "SECONDARY ICD CODE 7 DESCRIPTION": {"Secondary Diagnosis 7 - ICD 10 code description "},
        "SECONDARY ICD CODE 8 DESCRIPTION": {"Secondary Diagnosis 8 - ICD 10 code description "},
        "SECONDARY ICD CODE 9 DESCRIPTION": {"Secondary Diagnosis 9 - ICD 10 code description "},
        "SECONDARY ICD CODE 10 DESCRIPTION": {"Secondary Diagnosis 10 - ICD 10 code description "},
        "SECONDARY ICD CODE 11 DESCRIPTION": {"Secondary Diagnosis 11 - ICD 10 code description "},
        "SECONDARY ICD CODE 12 DESCRIPTION": {"Secondary Diagnosis 12 - ICD 10 code description "},
        "SECONDARY ICD CODE 13 DESCRIPTION": {"Secondary Diagnosis 13 - ICD 10 code description "},
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
        "ICD CODE DESCRIPTION" : {"Primary Diag Description"},
        "CPT CODE" : {"CPT Code"},
        "SECONDARY ICD CODE 1": {"2nd Diag Code"},
        "SECONDARY ICD CODE 2": {"3rd Diag Code"},
        "SECONDARY ICD CODE 3": {"4th Diag Code"},
        "SECONDARY ICD CODE 4": {"5th Diag Code"},
        "SECONDARY ICD CODE 5": {},
        "SECONDARY ICD CODE 6": {},
        "SECONDARY ICD CODE 7": {},
        "SECONDARY ICD CODE 8": {},
        "SECONDARY ICD CODE 9": {},
        "SECONDARY ICD CODE 10": {},
        "SECONDARY ICD CODE 11": {},
        "SECONDARY ICD CODE 12": {},
        "SECONDARY ICD CODE 13": {},
        "SECONDARY ICD CODE 1 DESCRIPTION": {},
        "SECONDARY ICD CODE 2 DESCRIPTION": {},
        "SECONDARY ICD CODE 3 DESCRIPTION": {},
        "SECONDARY ICD CODE 4 DESCRIPTION": {},
        "SECONDARY ICD CODE 5 DESCRIPTION": {},
        "SECONDARY ICD CODE 6 DESCRIPTION": {},
        "SECONDARY ICD CODE 7 DESCRIPTION": {},
        "SECONDARY ICD CODE 8 DESCRIPTION": {},
        "SECONDARY ICD CODE 9 DESCRIPTION": {},
        "SECONDARY ICD CODE 10 DESCRIPTION": {},
        "SECONDARY ICD CODE 11 DESCRIPTION": {},
        "SECONDARY ICD CODE 12 DESCRIPTION": {},
        "SECONDARY ICD CODE 13 DESCRIPTION": {},
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