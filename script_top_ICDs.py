
import pandas as pd

df = pd.read_csv("symptoms_coding_archive/modified_essential_symptoms_list_reviewed.csv")

icd_dict = {}

for index, row in df.iterrows():
    icd_desc = row["ICD Code"]
    avey_code_final = row["Avey code (final)"]
    avey_code_desc = row["Avey code description"]
    avey_code_doctor = row["Avey code (Doctor’s opinion)"]
    avey_desc_nlp = row["Avey Description (NLP)"]
    code_nlp_engine = row["Code in NLP engine (NLP)"]
    icd_dict[icd_desc] = (avey_code_final, avey_code_desc, avey_code_doctor, avey_desc_nlp, code_nlp_engine)

lst = [
('R104', 22045, {'other', 'other and unspecified abdominal pain'}),
('R509', 19278, {'fever,', 'fever, unspecified'}),
('R53', 18570, {'r53 malaise and fatigue', 'malaise and fatigue'}),
('R05', 16774, {'r05 cough', 'cough'}),
('R074', 14840, {'chest', 'chest pain, unspecified'}),
('R42', 11158, {'dizziness and giddiness', 'r42 dizziness and giddiness'}),
('R51', 10935, {'headache', 'r51 headache'}),
('R002', 8096, {'palpitations'}),
('R11', 6701, {'nausea and vomiting', 'r11 nausea and vomiting'}),
('R300', 5619, {'dysuria'}),
('R060', 5327, {'dyspnoea'}),
('R73', 4839, {'r73 elevated blood glucose level', 'elevated blood glucose level'}),
('R35', 3427, {'polyuria', 'r35 polyuria'}),
('R103', 3106, {'pain', 'pain localised to other parts of lower abdomen'}),
('R100', 2799, {'acute', 'acute abdomen'}),
('R070', 2320, {'pain', 'pain in throat'}),
('R529', 1921, {'pain, unspecified', 'pain,'}),
('R073', 1807, {'other chest pain', 'other'}),
('R80', 1536, {'r80 isolated proteinuria', 'isolated proteinuria'}),
('R101', 1515, {'pain', 'pain localised to upper abdomen'}),
('R252', 1317, {'cramp and spasm', 'cramp'}),
('R102', 1045, {'pelvic', 'pelvic and perineal pain'}),
('R12', 1017, {'r12 heartburn', 'heartburn'}),
('R829', 988, {'other and unspecified abnormal findings in urine', 'other'}),
('R062', 967, {'wheezing'}),
('R14', 966, {'r14 flatulence and related conditions', 'flatulence and related conditions'}),
('R030', 928, {'elevated', 'elevated blood-pressure reading, without diagnosis of hypertension'}),
('R202', 838, {'paraesthesia', 'paraesthesia of skin'}),
('R231', 825, {'pallor'}),
('R609', 823, {'oedema,', 'oedema, unspecified'}),
('R634', 779, {'abnormal weight loss', 'abnormal'}),
('R21', 752, {'rash and other nonspecific skin eruption', 'r21 rash and other nonspecific skin eruption'}),
('R520', 645, {'acute', 'acute pain'}),
('R071', 595, {'chest', 'chest pain on breathing'}),
('R631', 568, {'polydipsia'}),
('R000', 496, {'tachycardia,', 'tachycardia, unspecified'}),
('R309', 480, {'painful', 'painful micturition, unspecified'}),
('R221', 452, {'localised swelling, mass and lump, neck', 'localised'}),
('R31', 443, {'unspecified haematuria', 'r31 unspecified haematuria'}),
('R068', 435, {'other and unspecified abnormalities of breathing', 'other'}),
('R55', 414, {'syncope and collapse', 'r55 syncope and collapse'}),
('R229', 391, {'localised swelling, mass and lump, unspecified', 'localised'}),
('R508', 378, {'other specified fever', 'other'}),
('R635', 360, {'abnormal weight gain', 'abnormal'}),
('R224', 354, {'localised swelling, mass and lump, lower limb', 'localised'}),
('R600', 352, {'localised oedema', 'localised'}),
('R040', 347, {'epistaxis'}),
('R682', 328, {'dry mouth, unspecified', 'dry'}),
('R198', 327, {'other specified symptoms and signs involving the digestive system and abdomen', 'other'}),
('R900', 327, {'intracranial', 'intracranial space-occupying lesion'}),
('R0989', 317, {'other specified symptoms and signs involving the respiratory system', 'other'}),
('R001', 277, {'bradycardia, unspecified', 'bradycardia,'}),
('R251', 267, {'tremor, unspecified', 'tremor,'}),
('R194', 189, {'change', 'change in bowel habit'}),
('R195', 185, {'other faecal abnormalities', 'other'}),
('R391', 179, {'other difficulties with micturition', 'other'}),
('R630', 167, {'anorexia'}),
('R0988', 159, {'other', 'other specified symptoms and signs involving the circulatory system'}),
('R13', 147, {'r13 dysphagia', 'dysphagia'}),
('R223', 129, {'localised swelling, mass and lump, upper limb', 'localised'}),
('R160', 113, {'hepatomegaly, not elsewhere classified', 'hepatomegaly,'}),
('R011', 112, {'cardiac', 'cardiac murmur, unspecified'}),
('R222', 97, {'localised swelling, mass and lump, trunk', 'localised'}),
('R32', 96, {'r32 unspecified urinary incontinence', 'unspecified urinary incontinence'}),
('R220', 96, {'localised swelling, mass and lump, head', 'localised'}),
('R072', 70, {'precordial pain', 'precordial'}),
('R638', 65, {'other symptoms and signs concerning food and fluid intake', 'other'}),
('R238', 64, {'other and unspecified skin changes', 'other'}),
('R943', 64, {'abnormal results of cardiovascular function studies', 'abnormal'}),
('R398', 64, {'other and unspecified symptoms and signs involving the urinary system', 'other'}),
('R599', 63, {'enlarged lymph nodes, unspecified', 'enlarged'}),
('R008', 62, {'other and unspecified abnormalities of heart beat', 'other'}),
('R233', 60, {'spontaneous ecchymoses', 'spontaneous'}),
('R522', 59, {'other chronic pain', 'other'}),
('R042', 57, {'haemoptysis'}),
('R193', 57, {'abdominal rigidity', 'abdominal'}),
('R590', 56, {'localised enlarged lymph nodes', 'localised'}),
('R770', 56, {'abnormality of albumin', 'abnormality'}),
('R946', 52, {'abnormal', 'abnormal results of thyroid function studies'}),
('R498', 51, {'other and unspecified voice disturbances', 'other'}),
('R190', 51, {'intra-abdominal and pelvic swelling, mass and lump', 'intra-abdominal'}),
('R10', 50, {'abdominal and pelvic pain'}),
('R611', 46, {'generalised hyperhidrosis', 'generalised'}),
('R270', 45, {'ataxia, unspecified', 'ataxia,'}),
('R632', 43, {'polyphagia'}),
('R091', 43, {'pleurisy'}),
('R871', 43, {'abnormal', 'abnormal findings in specimens from female genital organs, abnormal level of hormones'})
]

res = []
for elem in lst:
    try:
        res.append((elem[0], elem[1], icd_dict[elem[0]]))
    except:
        pass

for elem in res:
    if str(elem[2][1]) == 'nan' and str(elem[2][0]) != 'nan':
        print(elem)