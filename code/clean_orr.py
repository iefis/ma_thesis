# last modified: Feb 29th, 2024
# clean ORR data
import pandas as pd
# read-in data
data_dir = 'U:\data'
df_75_90 = pd.read_csv(data_dir+"\\orr_ind_1975_1990.csv",low_memory=False)
df_91_08 = pd.read_csv(data_dir+"\\orr_ind_1991_2008.csv",low_memory=False)
df_orr = pd.concat([df_75_90, df_91_08])
print(df_orr.head())
df_orr['age'] = df_orr['year'] - df_orr['birth_year']
# remember to include only female population!
df_orr_sub = df_orr.loc[(df_orr['sex'] == 'female') & (df_orr['age'] >= 18) & (df_orr['age'] <= 65), 
                        ['year', 'id', 'statefp10', 'countyfp10']]
df_orr_sub = df_orr_sub.dropna()
df_orr_sub['statefp10'] = df_orr_sub['statefp10'].astype(int)
df_orr_sub['countyfp10'] = df_orr_sub['countyfp10'].astype(int)
year_county_orr = df_orr_sub.groupby(['year', 'statefp10', 'countyfp10']).count()
year_county_orr = year_county_orr.rename(columns={'id': 'count'})
year_county_orr.reset_index(inplace=True)

df_orr_cntry = df_orr.loc[(df_orr['sex'] == 'female') & (df_orr['age'] >= 18) & (df_orr['age'] <= 65), 
                        ['year', 'id','citizenship_stable']]
df_orr_cntry = df_orr_cntry.dropna()
country_year_orr = df_orr_cntry.groupby(['year', 'citizenship_stable']).count()
country_year_orr.to_csv(data_dir+"\\country_year_orr.csv", index=True)

year_county_orr.to_csv(data_dir+'\\year_county_orr.csv', index=None)