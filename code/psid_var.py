# %% [markdown]
# Construct the dictionary of PSID variables needed

# %%
import pandas as pd
import re
import json

data_dir = 'U:\data'

with open(data_dir+'\\PSID_variables.csv',"r", encoding='utf-8-sig') as f:
    var_dict = {}
    for row in f.readlines():
        name = re.search(r"\w*.*\,", row).group(0).strip(",")
        yrs = re.findall(r"\[\d{2}\]", row)
        vars = re.findall(r"[A-Z]+\w+", row)
        
        lst = []
        for i, yr in enumerate(yrs):
            yr = int(yr.strip(r"[\[\]]"))
            if yr >= 68:
                yr = 1900 + yr
            elif yr <= 21:
                yr = 2000 + yr
            lst.append([vars[i], yr])
        var_dict[name] = var_dict.get(name, []) + lst

with open(data_dir+"\\var_dict.json", "w") as f:    
    json.dump(var_dict, f)

