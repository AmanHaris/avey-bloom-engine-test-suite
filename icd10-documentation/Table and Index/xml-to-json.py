import xml.etree.ElementTree as ET
import json
from collections import defaultdict

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

# Load and parse the XML file
tree = ET.parse('icd10cm_tabular_2024.xml')
root = tree.getroot()

# Convert the parsed XML to a dictionary
xml_dict = etree_to_dict(root)

# Convert dictionary to a JSON string
json_data = json.dumps(xml_dict, indent=4)

# Optionally, write the JSON data to a file
with open('icd10cm_tabular_2024.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
