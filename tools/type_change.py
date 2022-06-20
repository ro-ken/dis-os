import json

def DictToBytes(data_dict,encoding):
    """字典转为字节流"""
    if type(data_dict) != dict:
        return None
    return json.dumps(data_dict).encode(encoding)

def BytesToDict(data_bytes):
    """字节流转为字典"""
    if type(data_bytes) != bytes:
        return None
    return json.loads(data_bytes)