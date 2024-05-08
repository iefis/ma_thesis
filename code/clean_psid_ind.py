# last modified: Mar 3rd, 2024
# clean PSID individual data
import pandas as pd
import json
# read-in data
data_dir = 'U:\data'
df_ind = pd.read_csv(data_dir+'\\psid_ind.csv')


# read in variable dictionary
with open(data_dir+"\\var_dict.json", "r") as f:
    var_dict = json.load(f)

rename_fam_dict = {}
rename_ind_dict = {}
for key, vals in var_dict.items():
    for val in vals:
        if val[0] in df_ind.columns: 
            rename_ind_dict[val[0]] = key+str(val[1])
        else:
            rename_fam_dict[val[0]] = key+str(val[1])

# print(rename_ind_dict)
df_ind = df_ind[df_ind.columns[df_ind.columns.isin(rename_ind_dict)]]
df_ind = df_ind.rename(columns=rename_ind_dict)
print(df_ind.head())
# set ID to each individual
df_ind["ID"] = df_ind.reset_index().index

# get next period's working hours
# drop invalid rows based on number of hours worked
for i in range(1968, 1993):
    hrs_work = "hrs_work" + str(i)
    hrs_work_1 =  "hrs_work" + str(i+1)
    df_ind[hrs_work] = df_ind[hrs_work_1] 
    df_ind.loc[(df_ind[hrs_work] < 1) | (df_ind[hrs_work] > 5840), hrs_work] = None 
    print(df_ind[hrs_work].describe())
# df_ind.loc[(df_ind["wks_work2007"] < 1) | (df_ind["wks_work2007"] > 52), "wks_work2007"] = None
# df_ind.loc[(df_ind["hrs_work_wk2007"] < 1) | (df_ind["hrs_work_wk2007"] > 112), "hrs_work_wk2007"] = None
for yr in [1999, 2001, 2003, 2005]:
    hrs_work = "hrs_work" + str(yr)
    wks_work = "wks_work" + str(yr+2)
    hrs_work_wk = "hrs_work_wk" + str(yr+2)
    df_ind.loc[(df_ind[wks_work] < 1) | (df_ind[wks_work] > 52), wks_work] = None
    df_ind.loc[(df_ind[hrs_work_wk] < 1) | (df_ind[hrs_work_wk] > 112), hrs_work_wk] = None
    print(df_ind[wks_work].describe())
    print(df_ind[hrs_work_wk].describe())
    df_ind[hrs_work] = df_ind[wks_work] * df_ind[hrs_work_wk]
    print(df_ind[hrs_work].describe())

df_ind = df_ind.drop(columns=["wks_work1999","wks_work2001", "wks_work2003","wks_work2005", "wks_work2007", \
                    "hrs_work_wk1999","hrs_work_wk2001", "hrs_work_wk2003","hrs_work_wk2005","hrs_work_wk2007", "hrs_work1993"])
df_ind_long = pd.wide_to_long(df_ind, ['relationship', 'age', 'marital_pair', 'edu', 'housework', 'employment', 'hrs_work','family_id'],
                         i=['ID','marital_status1968','sex1968'], j="year")
print(df_ind_long.head())

df_ind_long.to_csv(data_dir+"\\psid_ind_long.csv")