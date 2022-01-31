from datetime import datetime

import os

data_folder = 'data'
eco_file = os.path.join(data_folder, 'lagdp1221_fixed.csv')
pop_data_file = os.path.join(data_folder, 'co-est2019-alldata.csv')
early_pop_data_file = os.path.join(data_folder, 'sub-est00int.csv')

available_units_folder = os.path.join(data_folder, 'available_units_data')
zillow_history_file = os.path.join(data_folder, 'Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
zillow_prediction_file = os.path.join(data_folder, 'zhvf_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
out_folder = os.path.join('outputs', datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
os.mkdir(out_folder)

num_top_eco_counties = 300
meta_file = 'meta.json'

