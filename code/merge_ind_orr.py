# last modified: Feb 29th, 2024
# merge PSID individual data with orr data
import pandas as pd

# read-in data
data_dir = 'U:\data'
df_ind = pd.read_csv(data_dir+'\\psid_ind_fam.csv')
print(df_ind.info())
psid_geocode = pd.read_csv(data_dir+"\\psid_geocode.csv")
psid_geocode = psid_geocode.rename(columns={"YEAR10":"year","FAMID10":"family_id"})
print(psid_geocode.head())
df_orr = pd.read_csv(data_dir+"\\year_county_orr.csv")
df_orr = df_orr.rename(columns={'statefp10':'STATE10','countyfp10':'COUNTY10'})
print(df_orr.head())
# merge geocode
df_ind_merge = df_ind.merge(psid_geocode, how="left", on=["year","family_id"])

# merge orr
df_ind_orr = df_ind_merge.merge(df_orr, how="left", on=['year','STATE10','COUNTY10'])


# clean the data
df_ind_orr_sub = df_ind_orr.loc[ # (df_ind_orr['sex1968']==2) 
                                (df_ind_orr['age']<=65) & (df_ind_orr['age']>=18)
                                & (df_ind_orr['relationship'] != 0) 
                                & (df_ind_orr['edu'] >= 1) & (df_ind_orr['edu'] <= 12)
                                & (df_ind_orr['STATE10']<= 98) & (df_ind_orr['COUNTY10']<= 998) , :]

print(df_ind_orr_sub.info())

df_ind_orr_sub.to_csv(data_dir+"\\ind_orr_sub.csv",index=None)