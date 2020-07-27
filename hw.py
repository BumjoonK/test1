import json
import sys

def to_json(file_name: str)->None:
    ret=[file_name]
    with open(file_name,"r") as handle:
        json.dump(file_name, handle, indent=4)
        
    file_name=sys.argv[1]
    ret=to_json(ret)
    print(ret)

