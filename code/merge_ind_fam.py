import pandas as pd

# read-in data
data_dir = 'U:\data'
df_ind_long = pd.read_csv(data_dir+"\\psid_ind_long.csv")
print(df_ind_long.info())
df_fam = pd.read_csv(data_dir+"\\psid_fam.csv")

# merge with family-level data
df_ind_long.loc[df_ind_long['relationship']==0, "relationship"] = None
df_ind_long.loc[df_ind_long['family_id']==0, 'family_id'] = None

df_fam = df_fam.rename(columns={'fam_id': 'family_id'})
df_fam.loc[(df_fam['family_id']==0), "family_id"] = None
df_fam = df_fam.drop(columns=["Unnamed: 0"])
print(df_fam.info())

df_ind_fam = df_ind_long.merge(df_fam, how="left", on=['year', 'family_id'])
print(df_ind_fam.head())
df_ind_fam['occupation'] = None
df_ind_fam.loc[((df_ind_fam['relationship']==1)|(df_ind_fam['relationship']==10)) &
                 (df_ind_fam['wife_in_fu']!=3), 'occupation'] = df_ind_fam['occupation_head_recode']
df_ind_fam.loc[((df_ind_fam['relationship']==2)|(df_ind_fam['relationship']==20)) & 
                (df_ind_fam['wife_in_fu']==1), 'occupation'] = df_ind_fam['occupation_spouse_recode']
df_ind_fam.loc[((df_ind_fam['relationship']==9)|(df_ind_fam['relationship']==90)) & 
                (df_ind_fam['wife_in_fu']==3), 'occupation'] = df_ind_fam['occupation_spouse_recode']
df_ind_fam['industry'] = None
df_ind_fam.loc[((df_ind_fam['relationship']==1)|(df_ind_fam['relationship']==10)) & 
                (df_ind_fam['wife_in_fu']!=3), 'industry'] = df_ind_fam['industry_head_recode']
df_ind_fam.loc[((df_ind_fam['relationship']==2)|(df_ind_fam['relationship']==20)) & 
                (df_ind_fam['wife_in_fu']==1), 'industry'] = df_ind_fam['industry_spouse_recode']
df_ind_fam.loc[((df_ind_fam['relationship']==9)|(df_ind_fam['relationship']==90)) & 
                (df_ind_fam['wife_in_fu']==3), 'industry'] = df_ind_fam['industry_spouse_recode']
print(df_ind_fam.head())
# occupation_mobility
df_ind_fam.sort_values(by=['ID','year'], inplace=True)
df_ind_fam['lagged_occupation'] = df_ind_fam.groupby('ID')['occupation'].shift(1)
df_ind_fam['occupation_mobility'] = None
df_ind_fam.loc[(df_ind_fam['lagged_occupation']!=df_ind_fam['occupation']), 'occupation_mobility'] = 1
df_ind_fam.loc[(df_ind_fam['lagged_occupation']==df_ind_fam['occupation']), 'occupation_mobility'] = 0
df_ind_fam.loc[(df_ind_fam['lagged_occupation'].isna()) | (df_ind_fam['occupation'].isna()), 'occupation_mobility'] = None
# the more positive, the more upward the occupation mobility has lead to; similar for the negative values
df_ind_fam['occ_change'] = df_ind_fam['occupation'] - df_ind_fam['lagged_occupation'] 
print(df_ind_fam.info())
df_ind_fam.to_csv(data_dir+"\\psid_ind_fam.csv", index=False) 