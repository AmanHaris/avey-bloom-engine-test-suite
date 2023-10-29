
# changes a list of dict into a dict of lists collected based on a single key
def combineByKey(dict_list, dict_keys):
    res = {}
    for entry in dict_list:
        key_val = ""
        for k in dict_keys:
            try:
                key_val += entry[k]
            except:
                raise Exception(f"key {k} not in subclaim")

        if key_val in res:
            res[key_val].append(entry)
        else:
            res[key_val] = [entry]
    return res