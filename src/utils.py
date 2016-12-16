import json

def load_config(path):
    # Load file as dictionary
    with open(path, 'r') as f:
        json_obj = json.load(f)

    # Convert keys and values from unicode to str
    ret = {}
    for key, value in json_obj.iteritems():
        if isinstance(key, unicode):
            key = str(key)
        if isinstance(value, unicode):
            value = str(value)
        ret[key] = value
    return ret
