
# changes a list of dict into a dict of lists collected based on a single key
def combineByKey(dict_list, dict_key, dict_key2 = None):
    res = {}
    for entry in dict_list:
        key_val = entry[dict_key]
        if dict_key2:
            key_val += entry[dict_key2]
        if key_val in res:
            res[key_val].append(entry)
        else:
            res[key_val] = [entry]
    return res