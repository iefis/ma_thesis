# last modified: Feb 29th, 2024
# clean sample data
import pandas as pd
import numpy as np
# read-in data
data_dir = 'U:\data'
df_sample = pd.read_csv(data_dir+'\\ind_orr_sub.csv')
# region
df_sample = df_sample[df_sample['CBSA10']<=49820] # drop the individuals with unknow geolocation or in foreign countries
# 1:northeast, 2:midwest, 3:south, 4:west, 5:foreign
region_dict = {1: [9,23,25,33,44,50,34,36,42], 2:[18,17,26,39,55,19,20,27,29,31,38,46],
                3:[10,11,12,13,24,37,45,51,54,1,21,28,47,5,22,40,48], 
                4:[4,8,16,35,30,49,32,56,2,6,15,41,53], 5:[98]}
region_dict_ = {'STATE10':[], 'region':[]}
for k, vs in region_dict.items():
    for v in vs:
        region_dict_['STATE10'].append(v)
        region_dict_['region'].append(k)
df_region = pd.DataFrame.from_dict(region_dict_)

df_sample = df_sample.merge(df_region, how="left", on="STATE10")

df_sample['region'] = df_sample['region'].astype('int64')
print(df_sample.info())
# merge cbsa
df_cbsa_count = df_sample[['CBSA10','count','year']].drop_duplicates().groupby(['CBSA10','year']).sum()
df_cbsa_count.reset_index(inplace=True)
df_cbsa_count = df_cbsa_count.rename(columns={'count':'count_cbsa'})
df_cbsa_count.loc[df_cbsa_count['count_cbsa']==None,'count_cbsa'] = 0

df_sample = df_sample.merge(df_cbsa_count, how="left", on=["CBSA10",'year'])

# marital status
marital_condition = [(df_sample['marital_status1968']==2),(df_sample['marital_status1968']==9),
                    (df_sample['marital_status1968']!=2) & (df_sample['marital_status1968']!=9)]
df_sample['never_married'] = np.select(marital_condition,[1,None,0])

# housework
df_sample['hous_production'] = 0
df_sample.loc[(df_sample['employment'] == 6),'hous_production'] = 1
df_sample.loc[(df_sample['employment'] == 9)|
            (df_sample['employment'] == 0),'hous_production'] = None 
# check if in the labor force
df_sample['laborforce'] = 1
df_sample.loc[(df_sample['employment'] == 4) | (df_sample['employment'] == 5)|
               (df_sample['employment'] == 7)| (df_sample['employment'] == 9)| 
                (df_sample['employment'] == 0)| (df_sample['employment'] == 6),'laborforce'] = 0
# only account for labor force
df_sample['temp_off'] = 0
df_sample.loc[(df_sample['laborforce'] == 0), "temp_off"] = None
df_sample.loc[(df_sample['employment'] == 2) , "temp_off"] = 1
df_sample['unemployed'] = 0
df_sample.loc[(df_sample['laborforce'] == 0), "unemployed"] = None
df_sample.loc[(df_sample['employment'] == 3), "unemployed"] = 1
df_sample['employed'] = 0
df_sample.loc[(df_sample['laborforce'] == 0), "employed"] = None
df_sample.loc[(df_sample['employment'] == 1), 'employed'] = 1

# create region-year FE
df_sample['reg_yr'] = df_sample['region'] * df_sample['year']

# create industry-year FE
df_sample['ind_yr'] = df_sample['industry'] * df_sample['year']

# sex
df_sample.loc[df_sample['sex1968']==9 ,'sex1968'] = None

# extract sample with relevant variables
df_sample = df_sample.loc[(df_sample['year'] > 1980) & (df_sample['year'] <= 2008), 
                    ['ID','year','sex1968','age','edu','employed', 'white',
                    'unemployed',"temp_off",'hous_production',
                    'CBSA10','reg_yr','ind_yr','hrs_work','STATE10',
                    'COUNTY10','count_cbsa','never_married','industry','occupation', 'occupation_mobility', 'occ_change']]
print(df_sample.info())
print(df_sample['hrs_work'].describe())
df_sample.to_csv(data_dir+"\\sample_ind.csv", index=None)