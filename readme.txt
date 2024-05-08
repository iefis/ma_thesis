-- cleaning
- clean_psid_varname.py (may not be necessary)
input:var_name.txt
output:var_list.csv

- psid_var.py
input:variables0229.csv
output:var_dict0301.json ---!!!!

- get_fam.py
input: var_dict0421.json
output: fam_command.txt

- clean_fam.py
input:FAM1981.csv,...,FAM2007.csv, var_dict0421.json
output:psid_fam.csv

- clean_psid_ind.py
input:psid_ind.csv; var_dict0301.json
output:psid_ind_long.csv

- merge_ind_fam.py
input: psid_ind_long.csv, psid_fam.csv
output: psid_ind_fam.csv

- merge_ind_orr.py
input:psid_ind_fam.csv
output:ind_orr_sub_new.csv 

- clean_sample.py
input:ind_orr_sub_new.csv
output:sample_ind_new.csv

- clean_orr.py
input:orr_ind_1975_1990.csv; orr_ind_1991_2008.csv
output:country_year_orr.csv; year_county_orr_new.csv

- clean_cps.py
input:cps_sub.csv; metro_1990.csv; matched_cbsa.csv; sample_ind_new.csv; country_year_orr.csv
output:sample_ind_IV_full.csv



-- analysis
- analysis.rmd
input: sample_ind_IV.csv