import json
import traceback

def dict_to_json(dictionary, filename):
    # """
    #     dictionary : |dict|
    #     filename : |string|
    #             path to output json file.
                
    #     Examples
    #     --------
    #     >>> dict_to_json({"test1" : [1,2,3,4,5]}, r"C:\Users\User\Downloads")
    # """
    try:
        with open(filename, "w") as outfile:
            json.dump(dictionary, outfile)
    except:
        traceback.print_exc()

def load_json(filename):
    # """
    #     filename : |string|
    #             path to json file.
                
    #     Examples
    #     --------
    #     >>> load_json('data.json')
    # """
    try:
        f = open(filename)
        data = json.load(f)
        return data
    except:
        traceback.print_exc()