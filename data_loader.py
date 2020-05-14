import os, json
import pandas as pd

path = "collect/fixtures/"

csv_file = pd.DataFrame(pd.read_csv(path + "App_No.csv", sep = ",", header = 0, index_col = False))
csv_file.to_json(path + "App_No_Temp.json", orient = "records", force_ascii = True)

with open(path + "App_No_Temp.json", 'r+') as json_file:
    decoded = json.load(json_file)
    for elem in decoded:
        elem['model'] = 'collect.applicant'
        elem['fields'] = {
            'name': 'default-name',
            'photo': 'default.png',
            'sign': 'default.png'
        }
        print(elem)

    with open(path + "App_No.json", 'w+') as out_file:
        json.dump(decoded, out_file, indent=4)

os.remove(path + "App_No_Temp.json")
