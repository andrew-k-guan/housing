import config

import matplotlib.pyplot as plt
import pandas as pd

import os

def get_eco_df():
	df = pd.read_csv(config.eco_file)
	             
	col_names = df.columns
	df = df.rename(columns = {
		col_names[0]: 'County',
		col_names[1]: '2017 Real',
		col_names[2]: '2018 Real',
		col_names[3]: '2019 Real',
		col_names[4]: '2020 Real',
		col_names[5]: 'State Rank Real',
		col_names[6]: '2018 Percent',
		col_names[7]: '2019 Percent',
		col_names[8]: '2020 Percent',
		col_names[9]: 'State Rank Percent',
	})
	df.dropna(axis='columns', how='all', inplace=True)
	df.dropna(axis='rows', how='any', inplace=True)
	df = df[df['2020 Real'] != '(NA)']
	df['2017 Real'] = pd.to_numeric(df['2017 Real'].str.replace(',', ''), errors='coerce')
	df['2018 Real'] = pd.to_numeric(df['2018 Real'].str.replace(',', ''), errors='coerce')
	df['2019 Real'] = pd.to_numeric(df['2019 Real'].str.replace(',', ''), errors='coerce')
	df['2020 Real'] = pd.to_numeric(df['2020 Real'].str.replace(',', ''), errors='coerce')
	df['State Rank Real'] = pd.to_numeric(df['State Rank Real'], errors='coerce')
	df['2018 Percent'] = pd.to_numeric(df['2018 Percent'], errors='coerce')
	df['2019 Percent'] = pd.to_numeric(df['2019 Percent'], errors='coerce')
	df['2020 Percent'] = pd.to_numeric(df['2020 Percent'], errors='coerce')
	df['State Rank Percent'] = pd.to_numeric(df['State Rank Percent'], errors='coerce')

	county_df = df.dropna(axis='rows', how='any')
	county_real_sorted = county_df.nlargest(config.num_top_eco_counties, '2020 Real')
	print('100th largest county by gdp:')
	print(county_real_sorted.values[-1])

	min_gdp = county_real_sorted.values[-1][4]
	min_gdp_df = county_df[county_df['2020 Real'] >= min_gdp]
	# min_gdp_df['2018 Rank'] = min_gdp_df['2018 Percent'].rank(ascending=False)
	# min_gdp_df['2019 Rank'] = min_gdp_df['2019 Percent'].rank(ascending=False)
	# min_gdp_df['2020 Rank'] = min_gdp_df['2020 Percent'].rank(ascending=False)
	return min_gdp_df


def get_pop_df():
	pop_df = pd.read_csv(config.pop_data_file, encoding='ISO-8859-1')
	#Remove state data
	pop_df = pop_df[pop_df['CTYNAME'].str.contains('County')]

	early_pop_df = pd.read_csv(config.early_pop_data_file, encoding='ISO-8859-1')
	pop_df = pop_df.merge(early_pop_df, left_on=['CTYNAME', 'STNAME'], right_on=['NAME', 'STNAME'], suffixes=(None, '_y'))
	pop_df['POPESTIMATE2020'] = pop_df['POPESTIMATE2019']

	return pop_df

def get_housing_unit_dfs(msas, msa_data, pop_df):
	totals = []
	one_units = []
	two_units = []
	three_units = []
	five_units = []
	structures = []
	pop_counts = []
	columns = ['POPESTIMATE' + str(i) for i in range(2000, 2021)]
	for msa in msas:
		if msa not in msa_data:
			continue
		counties = [county + ' County' for county in msa_data[msa]['Counties']]
		state = msa_data[msa].get('Housing_Unit_State', None)
		data = get_msa_data(msa_data[msa]['Housing_Unit_MSA'], state)
		totals.append(data[0])
		one_units.append(data[1])
		two_units.append(data[2])
		three_units.append(data[3])
		five_units.append(data[4])
		structures.append(data[5])
		pop_counts.append(
			list(pop_df[pop_df['CTYNAME'].isin(counties)][columns].sum())
			)

	columns = [pd.to_datetime('{}-12-31'.format(i)) for i in range(2000, 2021)]
	msa_idx = [msa for msa in msas if msa in msa_data]
	pop_counts = pd.DataFrame(pop_counts, dtype='int64', index=msa_idx, columns=columns)

	total = pd.DataFrame(totals, dtype='int64', index=msa_idx, columns=columns) / pop_counts
	one_units = pd.DataFrame(one_units, dtype='int64', index=msa_idx, columns=columns) / pop_counts
	two_units = pd.DataFrame(two_units, dtype='int64', index=msa_idx, columns=columns) / pop_counts
	three_units = pd.DataFrame(three_units, dtype='int64', index=msa_idx, columns=columns) / pop_counts
	five_units = pd.DataFrame(five_units, dtype='int64', index=msa_idx, columns=columns) / pop_counts
	structures = pd.DataFrame(structures, dtype='int64', index=msa_idx, columns=columns) / pop_counts

	return total, one_units, two_units, three_units, five_units, structures

def get_msa_data(msa, state):
	totals = []
	one_units = []
	two_units = []
	three_units = []
	five_units = []
	structures = []
	for i in range(2000, 2019):
		cur_file = os.path.join(config.available_units_folder, 'tb3u{}.txt'.format(i))
		with open(cur_file, 'r') as f:
			found_line = None
			use_next = False
			for line in f:
				if use_next:
					split = line.split()
					structures.append(int(split[-1]))
					five_units.append(int(split[-2]))
					three_units.append(int(split[-3]))
					two_units.append(int(split[-4]))
					one_units.append(int(split[-5]))
					totals.append(int(split[-6]))
					use_next = False
				else:
					if msa in line:
						if state is None or state in line:
							split = line.split()
							if found_line is None:
								found_line = line
								if len(split) < 7:
									use_next = True
								else:
									structures.append(int(split[-1]))
									five_units.append(int(split[-2]))
									three_units.append(int(split[-3]))
									two_units.append(int(split[-4]))
									one_units.append(int(split[-5]))
									totals.append(int(split[-6]))
							else:
								print('Multiple line found in file tb3u{}.txt: {}'.format(i, line))

	for i in range(2019, 2021):
		df = pd.read_csv(
			os.path.join(config.available_units_folder, 'msannual_{}'.format(i), 'MSA Units-Table 1.csv'),
			header=5)
		df.dropna(axis='columns', how='all', inplace=True)
		df.dropna(axis='rows', how='any', inplace=True)
		if state is not None:
			msa_name = msa + ", " + state
		else:
			msa_name = msa
		rows = df[df['Name'].str.contains(msa_name)]
		if len(rows) > 1:
			print('Multiple match found for msa {} in file msannual_{}:'.format(msa, i))
			print(rows)
		else:
			totals.append(rows['Total'].item())
			one_units.append(rows['1 Unit'].item())
			two_units.append(rows['2 Units'].item())
			three_units.append(rows['3 and 4 Units'].item())
			five_units.append(rows['5 Units or More'].item())
			structures.append(rows['Num of Structures With 5 Units or More'].item())

	return (totals, one_units, two_units, three_units, five_units, structures)

def get_zillow_forecast_data(msas):
	zillow_price_df = pd.read_csv(config.zillow_prediction_file)
	zillow_msa_df = zillow_price_df[zillow_price_df['Region'] == 'Msa']
	forecasted_date = zillow_msa_df['ForecastedDate'].mode()
	predicted_price = zillow_msa_df[zillow_msa_df['RegionName'].str.contains('|'.join(msas))][['RegionName', 'ForecastYoYPctChange']]
	predicted_price.sort_values('ForecastYoYPctChange', inplace=True, ascending=False)
	return predicted_price, forecasted_date.item()


def get_zillow_history_data(msas):
	df = pd.read_csv(config.zillow_history_file)
	df = df[df['RegionType'] == 'Msa']
	df = df[df['RegionName'].str.contains('|'.join(msas))]

	pct_df = pd.DataFrame()
	pct_df['RegionName'] = df['RegionName']
	date_cols = df.columns[5:]
	for i in range(len(date_cols) - 1):
		pct_df[date_cols[i + 1]] = (df[date_cols[i + 1]] - df[date_cols[i]]) / df[date_cols[i]] * 100

	df = df.melt(id_vars=['RegionName', 'RegionID', 'SizeRank', 'RegionType', 'StateName'], var_name='Date', value_name='Price').assign(Date = lambda x: pd.to_datetime(x['Date']))
	df_pvt = df.pivot_table(index='Date', columns='RegionName', values='Price')

	pct_df = pct_df.melt(id_vars=['RegionName'], var_name='Date', value_name='Price').assign(Date = lambda x: pd.to_datetime(x['Date']))
	pct_df_pvt = pct_df.pivot_table(index='Date', columns='RegionName', values='Price') * 12
	return df_pvt, pct_df_pvt
