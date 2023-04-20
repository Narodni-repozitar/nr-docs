"""
# for when search in lists [nested type in mapping] is allowed by queries
replaces lists with randmly chosen element
def sub_first_list_elements(cur_val):
    ret = {}
    if cur_val and isinstance(cur_val, list):
        cur_val = random.choice(cur_val)
    if isinstance(cur_val, dict):
        for k, v in cur_val.items():
            ret[k] = sub_first_list_elements(v)
    else:
        return cur_val
    return ret

def get_paths(cur_path, cur_val):
    ret_paths = []
    if isinstance(cur_val, dict):
        for k, v in cur_val.items():
            ret_paths += get_paths(f"{cur_path}.{k}", v)
    else:
        if cur_path.startswith('.'):
            cur_path = cur_path[1:]
        ret_paths.append(f"{cur_path}")
    return ret_paths
flattened = sub_first_list_elements(sample_metadata_list[0]["metadata"])
paths = get_paths("metadata", flattened)
"""


def _get_paths(cur_path, cur_val):
    ret_paths = []
    if isinstance(cur_val, list):
        return ret_paths
    elif isinstance(cur_val, dict):
        for k, v in cur_val.items():
            ret_paths += get_paths(f"{cur_path}.{k}", v)
    else:
        if cur_path.startswith("."):
            cur_path = cur_path[1:]
        ret_paths.append(f"{cur_path}")
    return ret_paths


def get_paths(prefix, data):
    return _get_paths(prefix, data)
