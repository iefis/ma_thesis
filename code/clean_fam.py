# merge occupation, industry and race info from family index files
# based on family interview number and household head(1 ~ 81-82, 10 ~ 83-) / spouse information(2 or 9 ~ 81-82, 20 or 90 ~ 83-)
import pandas as pd
import json
# read-in data
data_dir = 'U:\data'
# variable dictionary
with open(data_dir+"\\var_dict.json") as f:
    vardict = json.load(f)

# Occupation recode
recode70 = {1: (1, 246), 2: (260, 726), 3: (740, 984)}
recode00 = {1: (1, 354), 2: (470, 593, 620, 975), 3: (360, 465, 600, 613)}
recode70_exception = {2: [221, 170, 164, 163, 101, 56, 22, 924]}
recode00_exception = {3: [830, 975, 202, 350, 300, 326, 313, 21, 674, 675, 962, 751, 913, 960, 626, 673, 693],
                2: [455, 441, 600, 612, 613, 352, 263, 341, 81, 244, 54, 16, 462, 924], 1: [430, 666, 272, 790]}

# Industry recode
ind70 = {1: (17, 28), 2: (45, 398), 3: (407, 479), 4: (507, 698), 5: (707, 718), 6: (828, 897), 7:(807, 809),
            8: (727, 798), 9: (907, 937)}
ind00 = {1: (17, 29), 2: (37, 49, 77, 107, 399), 3: (57, 69, 607, 679), 4: (407, 579), 5: (687, 719),
            6: (727, 779), 7: (856, 869), 8: (786, 847, 877, 929), 9: (937, 987)}

# function for 1981 & 1982
def clean_df(yr):
    df = pd.read_csv(data_dir+"\\FAM"+str(yr)+".csv")
    col_name = []
    for var in df.columns:
        varname = [k for k in vardict if [str(var), yr] in vardict[k]][0]
        col_name.append(varname)
    df.columns = col_name
    df["year"] = yr
    
    # recode for race
    df.loc[(df['race']==9)|(df['race']==0), 'race'] = None
    df['white'] = df['race']
    df.loc[df['race']>1 ,'white'] = 0

    # recode for occupation and industry
    df.loc[(df['occupation_head']==0)|(df['occupation_head']==999), 'occupation_head'] = None
    df.loc[(df['occupation_spouse']==0)|(df['occupation_spouse']==999), 'occupation_spouse'] = None
    df.loc[(df['industry_head']==0)|(df['industry_head']==999), 'industry_head'] = None
    df.loc[(df['industry_spouse']==0)|(df['industry_spouse']==999), 'industry_spouse'] = None
    
    df['occupation_head_recode'] = None
    df['occupation_spouse_recode'] = None
    df['industry_head_recode'] = None
    df['industry_spouse_recode'] = None
    if yr <= 2001:
        # occupation
        df.loc[(df['occupation_head']<=recode70[1][1]) & (df['occupation_head']>=recode70[1][0]), 'occupation_head_recode'] = 1
        df.loc[(df['occupation_head']<=recode70[2][1]) & (df['occupation_head']>=recode70[2][0]), 'occupation_head_recode'] = 2
        df.loc[(df['occupation_head']<=recode70[3][1]) & (df['occupation_head']>=recode70[3][0]), 'occupation_head_recode'] = 3
        df.loc[df['occupation_head'].isin(recode70_exception[2]), 'occupation_head_recode'] = 2
        
        df.loc[(df['occupation_spouse']<=recode70[1][1]) & (df['occupation_spouse']>=recode70[1][0]), 'occupation_spouse_recode'] = 1
        df.loc[(df['occupation_spouse']<=recode70[2][1]) & (df['occupation_spouse']>=recode70[2][0]), 'occupation_spouse_recode'] = 2
        df.loc[(df['occupation_spouse']<=recode70[3][1]) & (df['occupation_spouse']>=recode70[3][0]), 'occupation_spouse_recode'] = 3
        df.loc[df['occupation_spouse'].isin(recode70_exception[2]), 'occupation_spouse_recode'] = 2
        # industry -- household head
        df.loc[(df['industry_head']<=ind70[1][1]) & (df['industry_head']>=ind70[1][0]), 'industry_head_recode'] = 1
        df.loc[(df['industry_head']<=ind70[2][1]) & (df['industry_head']>=ind70[2][0]), 'industry_head_recode'] = 2
        df.loc[(df['industry_head']<=ind70[3][1]) & (df['industry_head']>=ind70[3][0]), 'industry_head_recode'] = 3
        df.loc[(df['industry_head']<=ind70[4][1]) & (df['industry_head']>=ind70[4][0]), 'industry_head_recode'] = 4
        df.loc[(df['industry_head']<=ind70[5][1]) & (df['industry_head']>=ind70[5][0]), 'industry_head_recode'] = 5
        df.loc[(df['industry_head']<=ind70[6][1]) & (df['industry_head']>=ind70[6][0]), 'industry_head_recode'] = 6
        df.loc[(df['industry_head']<=ind70[7][1]) & (df['industry_head']>=ind70[7][0]), 'industry_head_recode'] = 7
        df.loc[(df['industry_head']<=ind70[8][1]) & (df['industry_head']>=ind70[8][0]), 'industry_head_recode'] = 8
        df.loc[(df['industry_head']<=ind70[9][1]) & (df['industry_head']>=ind70[9][0]), 'industry_head_recode'] = 9
        # industry -- spouse
        df.loc[(df['industry_spouse']<=ind70[1][1]) & (df['industry_spouse']>=ind70[1][0]), 'industry_spouse_recode'] = 1
        df.loc[(df['industry_spouse']<=ind70[2][1]) & (df['industry_spouse']>=ind70[2][0]), 'industry_spouse_recode'] = 2
        df.loc[(df['industry_spouse']<=ind70[3][1]) & (df['industry_spouse']>=ind70[3][0]), 'industry_spouse_recode'] = 3
        df.loc[(df['industry_spouse']<=ind70[4][1]) & (df['industry_spouse']>=ind70[4][0]), 'industry_spouse_recode'] = 4
        df.loc[(df['industry_spouse']<=ind70[5][1]) & (df['industry_spouse']>=ind70[5][0]), 'industry_spouse_recode'] = 5
        df.loc[(df['industry_spouse']<=ind70[6][1]) & (df['industry_spouse']>=ind70[6][0]), 'industry_spouse_recode'] = 6
        df.loc[(df['industry_spouse']<=ind70[7][1]) & (df['industry_spouse']>=ind70[7][0]), 'industry_spouse_recode'] = 7
        df.loc[(df['industry_spouse']<=ind70[8][1]) & (df['industry_spouse']>=ind70[8][0]), 'industry_spouse_recode'] = 8
        df.loc[(df['industry_spouse']<=ind70[9][1]) & (df['industry_spouse']>=ind70[9][0]), 'industry_spouse_recode'] = 9

    if yr >= 2003:
        # exclude military specific occupation
        df.loc[((df['occupation_head']>=980)|(df['occupation_spouse']==615)), 'occupation_head'] = None
        df.loc[((df['occupation_spouse']>=980)|(df['occupation_spouse']==615)), 'occupation_spouse'] = None

        # occupation -- household head
        df.loc[((df['occupation_head']<=recode00[1][1]) & (df['occupation_head']>=recode00[1][0])), 'occupation_head_recode'] = 1
        df.loc[(((df['occupation_head']<=recode00[2][1]) & (df['occupation_head']>=recode00[2][0])) | 
                ((df['occupation_head']<=recode00[2][3]) & (df['occupation_head']>=recode00[2][2]))), 'occupation_head_recode'] = 2
        df.loc[(((df['occupation_head']<=recode00[3][1]) & (df['occupation_head']>=recode00[3][0])) | 
                ((df['occupation_head']<=recode00[3][3]) & (df['occupation_head']>=recode00[3][2]))), 'occupation_head_recode'] = 3
        df.loc[df['occupation_head'].isin(recode00_exception[3]), 'occupation_head_recode'] = 3
        df.loc[df['occupation_head'].isin(recode00_exception[2]), 'occupation_head_recode'] = 2
        df.loc[df['occupation_head'].isin(recode00_exception[1]), 'occupation_head_recode'] = 1
        # occupation -- spouse
        df.loc[((df['occupation_spouse']<=recode00[1][1]) & (df['occupation_spouse']>=recode00[1][0])), 'occupation_spouse_recode'] = 1
        df.loc[(((df['occupation_spouse']<=recode00[2][1]) & (df['occupation_spouse']>=recode00[2][0])) | 
                ((df['occupation_spouse']<=recode00[2][3]) & (df['occupation_spouse']>=recode00[2][2]))), 'occupation_spouse_recode'] = 2
        df.loc[(((df['occupation_spouse']<=recode00[3][1]) & (df['occupation_spouse']>=recode00[3][0])) | 
                ((df['occupation_spouse']<=recode00[3][3]) & (df['occupation_spouse']>=recode00[3][2]))), 'occupation_spouse_recode'] = 3
        df.loc[df['occupation_spouse'].isin(recode00_exception[3]), 'occupation_spouse_recode'] = 3
        df.loc[df['occupation_spouse'].isin(recode00_exception[2]), 'occupation_spouse_recode'] = 2
        df.loc[df['occupation_spouse'].isin(recode00_exception[1]), 'occupation_spouse_recode'] = 1
        # industry -- household head
        df.loc[(df['industry_head']<=ind00[1][1]) & (df['industry_head']>=ind00[1][0]), 'industry_head_recode'] = 1
        df.loc[((df['industry_head']<=ind00[2][1]) & (df['industry_head']>=ind00[2][0])) | (df['industry_head']==ind00[2][2]) |
                ((df['industry_head']<=ind00[2][4]) & (df['industry_head']>=ind00[2][3])), 'industry_head_recode'] = 2
        df.loc[((df['industry_head']<=ind00[3][1]) & (df['industry_head']>=ind00[3][0])) | 
               ((df['industry_head']<=ind00[3][3]) & (df['industry_head']>=ind00[3][2])), 'industry_head_recode'] = 3
        df.loc[(df['industry_head']<=ind00[4][1]) & (df['industry_head']>=ind00[4][0]), 'industry_head_recode'] = 4
        df.loc[(df['industry_head']<=ind00[5][1]) & (df['industry_head']>=ind00[5][0]), 'industry_head_recode'] = 5
        df.loc[(df['industry_head']<=ind00[6][1]) & (df['industry_head']>=ind00[6][0]), 'industry_head_recode'] = 6
        df.loc[(df['industry_head']<=ind00[7][1]) & (df['industry_head']>=ind00[7][0]), 'industry_head_recode'] = 7
        df.loc[((df['industry_head']<=ind00[8][1]) & (df['industry_head']>=ind00[8][0])) |
               ((df['industry_head']<=ind00[8][3]) & (df['industry_head']>=ind00[8][2])), 'industry_head_recode'] = 8
        df.loc[(df['industry_head']<=ind00[9][1]) & (df['industry_head']>=ind00[9][0]), 'industry_head_recode'] = 9
        # industry -- spouse
        df.loc[(df['industry_spouse']<=ind00[1][1]) & (df['industry_spouse']>=ind00[1][0]), 'industry_spouse_recode'] = 1
        df.loc[((df['industry_spouse']<=ind00[2][1]) & (df['industry_spouse']>=ind00[2][0])) | (df['industry_spouse']==ind00[2][2]) |
                ((df['industry_spouse']<=ind00[2][4]) & (df['industry_spouse']>=ind00[2][3])), 'industry_spouse_recode'] = 2
        df.loc[((df['industry_spouse']<=ind00[3][1]) & (df['industry_spouse']>=ind00[3][0])) | 
               ((df['industry_spouse']<=ind00[3][3]) & (df['industry_spouse']>=ind00[3][2])), 'industry_spouse_recode'] = 3
        df.loc[(df['industry_spouse']<=ind00[4][1]) & (df['industry_spouse']>=ind00[4][0]), 'industry_spouse_recode'] = 4
        df.loc[(df['industry_spouse']<=ind00[5][1]) & (df['industry_spouse']>=ind00[5][0]), 'industry_spouse_recode'] = 5
        df.loc[(df['industry_spouse']<=ind00[6][1]) & (df['industry_spouse']>=ind00[6][0]), 'industry_spouse_recode'] = 6
        df.loc[(df['industry_spouse']<=ind00[7][1]) & (df['industry_spouse']>=ind00[7][0]), 'industry_spouse_recode'] = 7
        df.loc[((df['industry_spouse']<=ind00[8][1]) & (df['industry_spouse']>=ind00[8][0])) |
               ((df['industry_spouse']<=ind00[8][3]) & (df['industry_spouse']>=ind00[8][2])), 'industry_spouse_recode'] = 8
        df.loc[(df['industry_spouse']<=ind00[9][1]) & (df['industry_spouse']>=ind00[9][0]), 'industry_spouse_recode'] = 9
    df = df.drop(columns=['occupation_head', 'occupation_spouse', 'industry_head', 'industry_spouse', 'race'])
    return df

df_lst = []
for yr in list(range(1981, 1998)) + [1999, 2001, 2003, 2005, 2007]:
    df_lst.append(clean_df(yr))    
df_fam = pd.concat(df_lst)
df_fam.to_csv(data_dir+"\\psid_fam.csv")
