import json

def get_user_classes(email):
    f = open("classes.json", "r+")
    json_object=json.load(f)
    f.close()
    cls_dict = json_object
    
    if cls_dict:
        return cls_dict
    return None
