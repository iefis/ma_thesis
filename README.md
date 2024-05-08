# Refugee inflow and female labor supply

## Code & Data file needed
### Cleaning

- [**psid_var.py**](https://github.com/iefis/ma_thesis/blob/main/code/psid_var.py) \
Turn PSID variable list into a dictionary \
input: [PSID_variables.csv](https://github.com/iefis/ma_thesis/tree/main/data/PSID) \
output: var_dict.json

- [**get_fam.py**](https://github.com/iefis/ma_thesis/blob/main/code/get_fam.py) \
Get STATA command for getting the PSID family level data for each year needed \
input: var_dict.json \
output: fam_command.txt

- [**clean_fam.py**](https://github.com/iefis/ma_thesis/blob/main/code/clean_fam.py)  \
Clean PSID family data \
input: FAM1981.csv,...,FAM2007.csv, var_dict.json \
output: psid_fam.csv

- [**clean_psid_ind.py**](https://github.com/iefis/ma_thesis/blob/main/code/clean_psid_ind.py) \
Clean PSID individual data \
input: psid_ind.csv; var_dict.json \
output: psid_ind_long.csv

- [**merge_ind_fam.py**](https://github.com/iefis/ma_thesis/blob/main/code/merge_ind_fam.py) \
Merge PSID family and individual data \
input: psid_ind_long.csv, psid_fam.csv \
output: psid_ind_fam.csv

- [**clean_orr.py**](https://github.com/iefis/ma_thesis/blob/main/code/clean_orr.py) \
Clean ORR data
input: orr_ind_1975_1990.csv; orr_ind_1991_2008.csv  
([available for download here](https://www.refugeeresettlementdata.com/data.html) with
the raw data for Figure 1 in [ORR](https://github.com/iefis/ma_thesis/tree/main/data/ORR)) \
output: country_year_orr.csv; year_county_orr.csv

- [**merge_ind_orr.py**](https://github.com/iefis/ma_thesis/blob/main/code/merge_ind_orr.py) \
Merge individual-level data with ORR data \
input: psid_ind_fam.csv; year_county_orr.csv \
output: ind_orr_sub.csv 

- [**clean_sample.py**](https://github.com/iefis/ma_thesis/blob/main/code/clean_sample.py) \
Clean the main sample \
input: ind_orr_sub.csv \
output: sample_ind.csv

- [**clean_cps.py**](https://github.com/iefis/ma_thesis/blob/main/code/clean_cps.py) \
Clean CPS subsample data to construct IV and merge with the main sample and shock data \
input: 
cps_sub.csv (CPS variable list in [CPS](https://github.com/iefis/ma_thesis/tree/main/data/CPS)); 
metro_1990.csv; matched_cbsa.csv; sample_ind.csv; country_year_orr.csv \
output: sample_ind_IV.csv

### Analysis
- [**analysis.Rmd**](https://github.com/iefis/ma_thesis/blob/main/code/analysis.Rmd) \
input: sample_ind_IV.csv
