from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

import json
import os

import config
import data_utils
import graph_utils

out_folder = os.path.join(config.out_folder, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

with open('meta.json', 'r') as f:
	metadata = json.load(f)
msas = metadata['Msas']
msa_data = metadata['MSA_Data']

pop_df = data_utils.get_pop_df()
eco_df = data_utils.get_eco_df()
totals, one_units, two_units, three_units, five_units, structures = data_utils.get_housing_unit_dfs(msas, msa_data, pop_df)
zillow_msas = [msa_data[msa]['Zillow_MSA'] for msa in msas]
zillow_forecast_df, forecasted_date = data_utils.get_zillow_forecast_data(zillow_msas)
abs_zillow_history_df, pct_zillow_history_df = data_utils.get_zillow_history_data(zillow_msas)

graph_utils.generate_zillow_prediction_graphs(zillow_forecast_df, forecasted_date)
graph_utils.generate_time_series_graphs(msas, msa_data, pop_df, totals, abs_zillow_history_df, pct_zillow_history_df)

os.mkdir(os.path.join(config.out_folder, 'eco'))
os.mkdir(os.path.join(config.out_folder, 'pop'))
key_counties = []
for msa in msas:
	graph_utils.generate_eco_graphs(eco_df, msa, msa_data[msa]['Counties'], os.path.join(config.out_folder, 'eco', msa + '.png'))
	graph_utils.generate_pop_graphs(pop_df, msa, msa_data[msa]['Counties'], os.path.join(config.out_folder, 'pop', msa + '.png'))
	key_counties.append(msa_data[msa]['Counties'][0])

# counties = [county + ' County' for county in counties]
graph_utils.generate_eco_graphs(eco_df, 'All', key_counties, os.path.join(config.out_folder, 'eco_all.png'))
graph_utils.generate_pop_graphs(pop_df, 'All', key_counties, os.path.join(config.out_folder, 'pop_all.png'))

# for k, v in metadata.items():
# 	print('Generating data for area ' + k)
# 	if k != "All":
# 		print(v['Counties'])
# 		# utils.generate_eco_graphs(eco_df, k, v['Counties'], os.path.join('outputs', 'eco', k + '.png'))
# 		pop_counties = [county + ' County' for county in v['Counties']]
# 		# county_df = utils.generate_pop_graphs(pop_df, k, pop_counties, os.path.join('outputs', 'pop', k + '.png'), v['States'], show=False)
# 		# dfs.append(county_df)
# 	else:
# 		all_graph_name, all_graph_values = k, v


# graph_utils.generate_housing_supply_graphs(total, one_units, two_units, three_units, five_units, structures)




# Pop/Eco Data for all counties
# full_df = pd.concat(dfs)

# counties = [list(county.keys())[0] for county in all_graph_values['Counties']]
# pop_counties = [county + ' County' for county in counties]
# cities = [list(county.values())[0] for county in all_graph_values['Counties']]
# county_df = eco_df[eco_df['County'].isin(counties)]
# print(county_df)
# for c in all_graph_values['Counties']:
# 	county = list(c.keys())[0]
# 	city = list(c.values())[0]
# 	county_df.loc[county_df['County'] == county, 'County'] = city
# 	full_df.loc[full_df['CTYNAME'] == county + ' County', 'CTYNAME'] = city
# print(county_df[['County', '2018 Rank', '2019 Rank', '2020 Rank']].sort_values('2020 Rank'))
# utils.generate_eco_graphs(county_df, k, cities, os.path.join('outputs', 'eco', 'all.png'), )
# utils.generate_pop_graphs(full_df, all_graph_name, cities, os.path.join('outputs', 'pop', 'all.png'), show=True)


# Zillow Data
# utils.generate_zillow_forecast(msas, os.path.join('outputs', 'zillow'))
# utils.generate_zillow_history(msas, os.path.join('outputs', 'zillow'))
