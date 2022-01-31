import config

import matplotlib.pyplot as plt
import pandas as pd

import os

def generate_eco_graphs(eco_df, region_name, counties, out_file, show=False):
	county_df = eco_df[eco_df['County'].isin(counties)]
	county_df.drop(inplace=True, columns=['State Rank Real', 'State Rank Percent'])
	real_output = county_df[['County', '2017 Real', '2018 Real', '2019 Real', '2020 Real']]
	perc_output = county_df[['County', '2018 Percent', '2019 Percent', '2020 Percent']]
	# rank_output = county_df[['County', '2018 Rank', '2019 Rank', '2020 Rank']]

	fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
	fig.set_size_inches(10, 6)
	fig.suptitle(region_name + ' County Economic Stats')
	real_output.set_index('County').transpose().plot(ax=ax1, legend=False)
	perc_output.set_index('County').transpose().plot(ax=ax2)
	# rank_output.set_index('County').transpose().plot(ax=ax3, legend=False)
	# ax3.set_ylim(ax3.get_ylim()[::-1])
	ax1.set_ylabel('Real GDP')
	ax2.set_ylabel('Percentage Growth')
	# ax3.set_ylabel('Percentage Growth Rank')
	ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	plt.tight_layout()
	plt.savefig(out_file)
	if show:
		plt.show()
	else:
		plt.close()

def generate_pop_graphs(pop_df, region_name, counties, out_file, show=False):
	counties = [county + ' County' for county in counties]
	county_df = pop_df[pop_df['CTYNAME'].isin(counties)]
	birth_cols = ['CTYNAME']
	death_cols = ['CTYNAME']
	dom_cols = ['CTYNAME']
	int_cols = ['CTYNAME']
	labels = ['County']
	for i in range(2011, 2020):
		birth_cols.append('RBIRTH' + str(i))
		death_cols.append('RDEATH' + str(i))
		dom_cols.append('RDOMESTICMIG' + str(i))
		int_cols.append('RINTERNATIONALMIG' + str(i))
		labels.append(i)
	birth_output = county_df[birth_cols]
	death_output = county_df[death_cols]
	dom_output = county_df[dom_cols]
	int_output = county_df[int_cols]

	birth_output.columns = labels
	death_output.columns = labels
	dom_output.columns = labels
	int_output.columns = labels

	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
	fig.set_size_inches(10, 6)
	fig.suptitle(region_name + ' County Population Stats')
	birth_output.set_index('County').transpose().plot(ax=ax1, legend=False)
	death_output.set_index('County').transpose().plot(ax=ax2)
	dom_output.set_index('County').transpose().plot(ax=ax3, legend=False)
	int_output.set_index('County').transpose().plot(ax=ax4, legend=False)
	ax1.set_ylabel('Birth Rate')
	ax2.set_ylabel('Death Rate')
	ax3.set_ylabel('Domestic Migration Rate')
	ax4.set_ylabel('International Migration Rate')
	ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	plt.tight_layout()
	plt.savefig(out_file)
	if show:
		plt.show()
	else:
		plt.close()
	return county_df

def generate_housing_supply_graphs(total, one_units, two_units, three_units, five_units, structures, show=False):
	fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2)
	fig.set_size_inches(14, 10)
	fig.suptitle('Housing Units Build per MSA per person')
	total.transpose().plot(ax=ax1, legend=False)
	one_units.transpose().plot(ax=ax2)
	two_units.transpose().plot(ax=ax3, legend=False)
	three_units.transpose().plot(ax=ax4, legend=False)
	five_units.transpose().plot(ax=ax5, legend=False)
	structures.transpose().plot(ax=ax6, legend=False)
	ax1.set_xlabel('Year')
	ax2.set_xlabel('Year')
	ax3.set_xlabel('Year')
	ax4.set_xlabel('Year')
	ax5.set_xlabel('Year')
	ax6.set_xlabel('Year')

	ax1.set_ylabel('Total Units Built')
	ax4.set_ylabel('Three/Four Units Built')
	ax2.set_ylabel('One Unit')
	ax3.set_ylabel('Two Units')
	ax5.set_ylabel('Five or More Units')
	ax6.set_ylabel('Structures with 5+ Units')
	ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	plt.tight_layout()
	plt.savefig(out_file)
	if show:
		plt.show()
	else:
		plt.close()


def generate_zillow_history_graphs(abs_df, pct_df, show=False):
	fig, ax = plt.subplots()
	fig.set_size_inches(10, 6)

	abs_df.plot(ax=ax)
	ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax.ticklabel_format(axis='y', style='plain')
	plt.title('Historical Price Data')
	plt.tight_layout()
	plt.savefig(os.path.join(out_folder, 'zillow_history.png'))
	if show:
		plt.show()
	else:
		plt.close()

	fig, ax = plt.subplots()
	fig.set_size_inches(10, 6)

	pct_df.plot(ax=ax)
	plt.axhline(y=0, color='r', linestyle='-')
	ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax.ticklabel_format(axis='y', style='plain')
	ax.set_ylabel('Annual Appreciation Rate')
	plt.title('Historical Price Data Percentage Change')
	plt.tight_layout()
	plt.savefig(os.path.join(out_folder, 'zillow_history_percent.png'))
	if show:
		plt.show()
	else:
		plt.close()

def generate_zillow_prediction_graphs(pred_df, forecast_date, show=False):
	fig, ax = plt.subplots()
	fig.set_size_inches(10, 6)
	pred_df.plot(x='RegionName', y='ForecastYoYPctChange', kind='bar', ax=ax, rot=45)
	# predicted_price.set_index('RegionName').transpose().plot.bar(x='RegionName', ax=ax, rot=0)
	ax.get_legend().remove()
	# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax.set_ylabel('Forecast YoY Percent Change')
	plt.title('Forecast YoY Percent Change, One Year to {}'.format(forecast_date))
	plt.tight_layout()
	plt.savefig(os.path.join(config.out_folder, 'zillow_forecast_{}.png'.format(forecast_date)))
	if show:
		plt.show()
	else:
		plt.close()

def generate_time_series_graphs(msas, msa_data, pop_df, totals, abs_zillow_history_df, pct_zillow_history_df, show=False):
	fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1)
	fig.set_size_inches(14, 10)

	pop_dfs = []
	pop_cols = ['CTYNAME']
	for i in range(2000, 2021):
		pop_cols.append('POPESTIMATE{}'.format(i))

	for i, msa in enumerate(msas):
		counties = msa_data[msa]['Counties']
		counties = [county + ' County' for county in counties]
		county_df = pop_df[pop_df['CTYNAME'].isin(counties)]
		pop_output = county_df[pop_cols]
		summed_df = pop_output.sum()
		summed_df['CTYNAME'] = msa
		pop_dfs.append(summed_df.to_frame().transpose())

	full_pop_df = pd.concat(pop_dfs, axis=0)
	pct_df = pd.DataFrame()
	pct_df['CTYNAME'] = full_pop_df['CTYNAME']
	for i in range(2001, 2020):
		pct_df['{}'.format(i)] = (full_pop_df['POPESTIMATE{}'.format(i)] - full_pop_df['POPESTIMATE{}'.format(i - 1)]) / full_pop_df['POPESTIMATE{}'.format(i - 1)]
	pct_df.rename(columns={'CTYNAME': 'MSA'}, inplace=True)

	pct_df.sort_values('MSA', inplace=True)
	pct_df.set_index('MSA').transpose().plot(ax=ax1)
	ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax1.axhline(y=0, color='r', linestyle='-')
	ax1.set_ylabel('Pct Pop Diff')

	totals.sort_index(inplace=True)
	totals.transpose().plot(ax=ax2)
	ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax2.set_ylabel('Total New Housing Permits')

	abs_zillow_history_df.plot(ax=ax3)
	ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax3.set_ylabel('Abs Housing Price')

	pct_zillow_history_df.plot(ax=ax4)
	ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	ax4.axhline(y=0, color='r', linestyle='-')
	ax4.set_ylabel('Pct Housing Price')

	plt.tight_layout()
	plt.savefig(os.path.join(config.out_folder, 'full_history.png'))
	if show:
		plt.show()
	else:
		plt.close()