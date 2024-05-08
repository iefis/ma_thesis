# last modified: May 5th, 2024
# clean cps data
import pandas as pd
import numpy as np
# read-in data
data_dir = 'U:\data'
df_cps = pd.read_csv(data_dir+'\\cps_sub.csv')
df_cps = df_cps.loc[(df_cps['year']>=1975) & (df_cps['year']<=2008) & (df_cps['metarea']<9997) & (df_cps['bpl']>9900) & (df_cps['bpl']<96000),:]
print(df_cps['bpl'].describe())
print(df_cps.head())

metro_cross = pd.read_csv(data_dir+'\\metro_1990.csv')
metro_cross = metro_cross[['metro','fips']].drop_duplicates()
print(metro_cross.info())

df_cps_geo = df_cps[['year','county','metarea','bpl','yrimmig','asecwt']].merge(metro_cross, how="left", left_on='metarea', right_on='metro')
print(df_cps_geo.info())

# merge metro-1990 code with CBSA code (note that this matching may be imperfect)
print("merge metro-1990 code with CBSA code: ")
metro_cbsa = pd.read_csv(data_dir+"\\matched_cbsa.csv")
df_cps_geo = df_cps_geo.merge(metro_cbsa[['metro','CBSA Code']], how="left", left_on="metarea", right_on="metro")
df_cps_geo.loc[(df_cps_geo['metarea']<=4484) & (df_cps_geo['metarea']>=4480),'CBSA Code'] = 31080 # add CBSA code for LA
df_cps_geo.loc[(df_cps_geo['metarea']==6780),'CBSA Code'] = 40140 #riverside-san bernadino, CA
df_cps_geo.loc[(df_cps_geo['metarea']<=1605) & (df_cps_geo['metarea']>=1600),'CBSA Code'] = 16980 # Chicago
df_cps_geo.loc[(df_cps_geo['metarea']<=6162) & (df_cps_geo['metarea']>=6160),'CBSA Code'] = 37980 # Philly
df_cps_geo.loc[(df_cps_geo['metarea']<=2162) & (df_cps_geo['metarea']>=2160),'CBSA Code'] = 19820 # Detroit
df_cps_geo.loc[(df_cps_geo['metarea']<=1681) & (df_cps_geo['metarea']>=1680),'CBSA Code'] = 17460 # Cleveland, OH
df_cps_geo.loc[(df_cps_geo['metarea']<=7601) & (df_cps_geo['metarea']>=7600),'CBSA Code'] = 42660 # Seattle
df_cps_geo.loc[(df_cps_geo['metarea']<=2083) & (df_cps_geo['metarea']>=2080),'CBSA Code'] = 19740 # Denver
df_cps_geo.loc[(df_cps_geo['metarea']<=3003) & (df_cps_geo['metarea']>=3000),'CBSA Code'] = 24340 # Grand rapids, MI
df_cps_geo.loc[(df_cps_geo['metarea']<=6282) & (df_cps_geo['metarea']>=6280),'CBSA Code'] = 38300 # Pittsburgh
df_cps_geo.loc[(df_cps_geo['metarea']<=8781) & (df_cps_geo['metarea']>=8780),'CBSA Code'] = 47300 # Visalia
df_cps_geo.loc[(df_cps_geo['metarea']<=5082) & (df_cps_geo['metarea']>=5080),'CBSA Code'] = 33340 # Milwaukee
df_cps_geo.loc[(df_cps_geo['metarea']==3590),'CBSA Code'] = 27260 #Jacksonville, FL
df_cps_geo.loc[(df_cps_geo['metarea']==3163),'CBSA Code'] = 43900 #spartanburg, sc
df_cps_geo.loc[(df_cps_geo['metarea']<=3162)&(df_cps_geo['metarea']>=3160),'CBSA Code'] = 24860 # Greenville, sc


df_cps_geo = df_cps_geo.dropna(subset=['CBSA Code'])
df_cps_geo = df_cps_geo.rename(columns = {'CBSA Code': 'CBSA10'})
df_cps_geo['CBSA10'] = df_cps_geo['CBSA10'].astype(int)
df_cps_geo = df_cps_geo.drop(columns=['metro_y','metro_x'])
print(df_cps_geo.info())

# 1975 - 1980: top source countries - main analysis
bpl_dict = {'cambodia': 51100, 'iran':53000, 'iraq':53200,'somalia':60050,'poland':45500,'romania':4560, 'ethiopia':60044,
            'cuba': 25000, 'yugoslavia':45700,'laos':51300, 'ussr':46500,'vietnam':51800, 'afghanistan': 52000}

# # 1975 - 1980: more top source countries - sensitivity analysis
# bpl_dict = {'cambodia': 51100, 'iran':53000, 'iraq':53200,'somalia':60050,'poland':45500,'romania':4560, 'ethiopia':60044,'hungary':45400,
            # 'cuba': 25000, 'yugoslavia':45700,'laos':51300, 'ussr':46500,'vietnam':51800, 'afghanistan': 52000, 'czechoslovakia':45200}
bpl_lst = bpl_dict.values()

# IV
print("initialize df_iv: ")
base_sample = pd.read_csv(data_dir+"\\sample_ind_new.csv")
cbsa_lst = list(base_sample['CBSA10'].unique())
yr_lst = list(base_sample['year'].unique())
cbsa_yr = []
for cbsa in cbsa_lst:
    for yr in yr_lst:
        cbsa_yr.append([cbsa, yr])
df_iv = pd.DataFrame(cbsa_yr, columns=['CBSA10', 'year'])
print(df_iv)

# by-year refugee numbers 
print("by-year refugee numbers:")
country_year_orr = pd.read_csv(data_dir+"\\country_year_orr.csv")
country_year_orr = country_year_orr.rename(columns={'citizenship_stable':'cntry','id':'FRI_jt'}) 
country_year_orr = country_year_orr.loc[country_year_orr['cntry'].isin(bpl_dict),:]
print(country_year_orr.head())

df_iv = df_iv.merge(country_year_orr, how="left", on='year')
print(df_iv.head())

# country share by CBSA
jct_list = []
d_jct_list = []
for pl in bpl_dict:
    cntry = str(pl)
    df_cps_geo_pre = df_cps_geo.loc[(df_cps_geo['yrimmig'] <= 1980), ['bpl','asecwt','CBSA10']]
    df_cps_geo_pre[cntry] = 0
    df_cps_geo_pre.loc[df_cps_geo_pre['bpl']==bpl_dict[pl], cntry] = 1
    immig_jc = 'immig_'+cntry +'_c'
    df_cps_geo_pre[immig_jc] = df_cps_geo_pre[cntry] * df_cps_geo_pre['asecwt']      
    print(df_cps_geo_pre.tail())
    df_cps_cntry = df_cps_geo_pre[[immig_jc,"CBSA10"]].groupby(["CBSA10"]).sum()
    df_cps_cntry.reset_index(inplace=True)
    immig_j = df_cps_cntry[[immig_jc]].sum()[0]
    print(immig_j)
    if immig_j == 0:
        continue
    else:
        immig_share = cntry +'_share'
        df_cps_cntry[immig_share] = df_cps_cntry[immig_jc] / immig_j
        df_cps_cntry['cntry'] = cntry
        print(df_cps_cntry.head())
        df_iv = df_iv.merge(df_cps_cntry[["CBSA10",'cntry',immig_share]], how="left", on=["CBSA10",'cntry'])
        df_iv[str(pl)+'_jct'] = df_iv[str(pl)+'_share'] * df_iv['FRI_jt']
        df_iv[str(pl)+'_d_jct'] = (df_iv[str(pl)+'_share'] > 0) * df_iv['FRI_jt']
        df_iv['immig_j'] = immig_j ###
        jct_list.append(str(pl)+'_jct')
        d_jct_list.append(str(pl)+'_d_jct')

# get each year's refugee inflow number
year_orr = country_year_orr.groupby(['year']).sum()
year_orr.reset_index(inplace=True)

# get IV_ct
df_iv['IV_jct'] = df_iv[jct_list].sum(axis=1)
df_iv['IV_d_jct'] = df_iv[d_jct_list].sum(axis=1)  
df_iv.to_csv(data_dir+'\\df_iv.csv')
df_iv = df_iv.merge(year_orr, how="left", on="year")
df_iv_linear = df_iv[['CBSA10','year','IV_jct']].groupby(['CBSA10','year']).sum()
df_iv_linear.reset_index(inplace=True)
df_iv_discrete = df_iv[['CBSA10','year','IV_d_jct']].groupby(['CBSA10','year']).sum()
df_iv_discrete.reset_index(inplace=True)

print(df_iv_linear.head())
print(df_iv_linear.tail())
print(df_iv_discrete.head())
print(df_iv_discrete.tail())

base_sample = base_sample.merge(df_iv_linear, how="left", on=['CBSA10','year'])
base_sample = base_sample.merge(df_iv_discrete, how="left", on=['CBSA10','year'])
base_sample = base_sample.rename(columns={'IV_jct':'IV_ct', 'IV_d_jct':'IV_d_ct'})

base_sample.to_csv(data_dir+"\\sample_ind_IV.csv", index=None)



