import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from stqdm import stqdm
import geoip2.database

import db_connect as db


def statistics():
	st.title('Statistics')
	st.title('Server Settings')
	statistics_selection = st.selectbox('Statistics Options',
											 ['Main Statistics', 'Servers Hit By IP Statistics'])

	if statistics_selection == 'Main Statistics':
		main_statistics()
	if statistics_selection == 'Servers Hit By IP Statistics':
		servers_hit()

def main_statistics():
	st.title('Statistics')
	auth_logs = db.auth_logs_to_df()
	auth_logs['Hour'] = auth_logs['Time'].str.split(':').str[0]
	auth_logs = auth_logs.sort_values(['Hour'], ascending=True)




	#Side Bar
	result = st.sidebar.button('Load Data')
	if result:
		search()
	
	# Jumpbox Data
	jump_boxes = []
	jump_boxes_options = (auth_logs['Box'].unique().tolist())
	for i in jump_boxes_options:
	    jump_boxes.append(i)
	jump_boxes.sort()
	jump_boxes.insert(0, 'All')

	side_jumpbox = st.sidebar.selectbox('Servers', (jump_boxes))

	if side_jumpbox == 'All':
	    failed_logs = auth_logs.loc[auth_logs['Access'] == 'Failed']
	    pass_logs = auth_logs.loc[auth_logs['Access'] == 'Successful']

	else: 
	    for i in jump_boxes_options:
	        if side_jumpbox == i:
	            failed_logs = auth_logs.loc[auth_logs['Access'] == 'Failed']
	            pass_logs = auth_logs.loc[auth_logs['Access'] == 'Successful']

	            failed_logs = failed_logs.loc[auth_logs['Box'] == i]
	            pass_logs = pass_logs.loc[auth_logs['Box'] == i]
	        else:
	            pass

	# Country
	country_boxes = []
	pass_country_options = (pass_logs['Country'].unique().tolist())
	fail_country_options = (failed_logs['Country'].unique().tolist())


	for i in pass_country_options:
	    if i not in country_boxes:
	        country_boxes.append(i)
	for i in fail_country_options:
	    if i not in country_boxes:
	        country_boxes.append(i)
	    
	country_boxes.sort()
	country_count = len(country_boxes)
	country_boxes.insert(0, 'All')
	country_count = len(country_boxes) - 1
	country_text = 'Which Country ? Total = ' + str(country_count)
	side_country = st.sidebar.selectbox(country_text, (country_boxes))        


	if side_country == 'All':
	    pass

	else: 
	    for i in country_boxes:
	        if side_country == i:
	            failed_logs = failed_logs.loc[auth_logs['Country'] == i]
	            pass_logs = pass_logs.loc[auth_logs['Country'] == i]
	        else:
	            pass


	# city
	city_boxes = []
	pass_city_options = (pass_logs['City'].unique().tolist())
	fail_city_options = (failed_logs['City'].unique().tolist())


	for i in pass_city_options:
	    if i not in city_boxes:
	        city_boxes.append(i)
	for i in fail_city_options:
	    if i not in city_boxes:
	        city_boxes.append(i)
	    
	city_boxes.sort()   
	city_boxes.insert(0, 'All')
	city_count = len(city_boxes) - 1
	city_text = 'Which City ? Total = ' + str(city_count)
	side_city = st.sidebar.selectbox(city_text, (city_boxes))      

	if side_city == 'All':
	    pass

	else: 
	    for i in city_boxes:
	        if side_city == i:
	            failed_logs = failed_logs.loc[auth_logs['City'] == i]
	            pass_logs = pass_logs.loc[auth_logs['City'] == i]
	        else:
	            pass    
	    
	    
	    
	    
	# Dates
	d = datetime.today() - timedelta(days=7)

	dates = []
	pass_date_options = (pass_logs['Date'].unique().tolist())
	fail_date_options = (failed_logs['Date'].unique().tolist())

	for i in pass_date_options:
	    if i not in dates:
	        dates.append(i)
	for i in fail_date_options:
	    if i not in dates:
	        dates.append(i)     

	all_dates_check = st.sidebar.checkbox('All Dates')

	if all_dates_check:
		pass

	else:
		try:
			layout = st.sidebar.columns([2, 1])
			

			min_date = min(dates)
			year = min_date.split('/')[0]
			month = min_date.split('/')[1]
			date = min_date.split('/')[2]

			min_date_time = datetime(int(year), int(month), int(date))

			with layout[0]: 
			    start_date = st.date_input('Start Date:',max_value=datetime.today()) # omit "sidebar"
			with layout[0]: 
			    end_date = st.date_input('End Date:',value=(d), min_value = min_date_time,max_value=datetime.today()) # omit "sidebar"

			new_start = str(start_date).replace('-','/')
			new_end = str(end_date).replace('-','/')
			pass_logs = pass_logs[(pass_logs['Date'] > new_end) & (pass_logs['Date'] <= new_start)]
			failed_logs = failed_logs[(failed_logs['Date'] > new_end) & (failed_logs['Date'] <= new_start)]
		except:
			pass
	st.sidebar.image('Images/Ned_Logo_Pictorial_T.png')

	dates = []
	all_dates = (auth_logs['Date'].unique().tolist())
	for i in all_dates:
	    dates.append(i)
	dates.sort()

	st.header('Successful Access Dates')
	pass_access_datedf = pass_logs
	pass_access_datedf = pass_access_datedf.groupby('Date')['Time'].nunique()
	pass_access_date_df = pd.DataFrame(pass_access_datedf).reset_index()
	pass_access_date_df.rename({'Time':'Count'}, axis=1, inplace=True)
	st.altair_chart(alt.Chart(pass_access_date_df).mark_bar().encode(
		x=alt.X('Date',scale=alt.Scale(nice=False)),
		y=alt.Y('Count'),
		tooltip=['Date','Count']
		).configure_mark(
		opacity=0.2,
		color='green',
		),
	use_container_width=True)

	try:
		st.header('Unsuccessful Access Dates')
		failed_access_datedf = failed_logs
		failed_access_datedf = failed_access_datedf.groupby('Date')['Time'].nunique()
		failed_access_date_df = pd.DataFrame(failed_access_datedf).reset_index()
		failed_access_date_df.rename({'Time':'Count'}, axis=1, inplace=True)
		st.altair_chart(alt.Chart(failed_access_date_df).mark_bar().encode(
			x=alt.X('Date',scale=alt.Scale(nice=False)),
			y=alt.Y('Count'),
			tooltip=['Date','Count']
			).configure_mark(
			opacity=0.2,
			color='red',
			),
		use_container_width=True)
	except:
		pass

	try:
		st.set_option('deprecation.showPyplotGlobalUse', False)
		st.header('Unsuccessful Access Times')
		failed_timedf = failed_logs
		failed_timedf[['Hour','Minute','Second']] = failed_logs['Time'].str.split(':', 3, expand=True)
		failed_time_hour = failed_timedf.groupby('Hour')['Time'].nunique()
		failed_hour_df = pd.DataFrame(failed_time_hour).reset_index()
		failed_hour_df.rename({'Time':'Count'}, axis=1, inplace=True)
		st.altair_chart(alt.Chart(failed_hour_df).mark_bar().encode(
			x=alt.X('Hour',scale=alt.Scale(nice=False)),
			y=alt.Y('Count'),
			tooltip=['Hour','Count']
			).configure_mark(
			opacity=0.2,
			color='red',
			),
		use_container_width=True)
	except:
		pass

	try:
		box_fail = failed_logs.groupby('Box')['Time'].nunique()
		box_fail_df = box_fail.to_frame()
		box_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
		box_fail_df = box_fail_df.reset_index()
		box_fail_df = box_fail_df.sort_values(by='Count', ascending=False)

		st.header('Box Unsuccessful Access Count')
		st.table(box_fail_df.set_index('Box'))
	except:
		pass

	try:
		country_fail = failed_logs.groupby('Country')['Time'].nunique()
		country_fail_df = country_fail.to_frame()
		country_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
		country_fail_df = country_fail_df.reset_index()
		country_fail_df = country_fail_df.sort_values(by='Count', ascending=False)
		country_fail_list = country_fail_df.index.tolist()
		country_list_count = len(country_fail_list)

		st.header('Country Unsuccessful Access Count')
		country_count_slider = st.slider('Country Count', max_value=country_list_count, value=5)
		st.table(country_fail_df.head(country_count_slider).set_index('Country'))
	except:
		pass

	try:
		city_fail = failed_logs.groupby(['City','Country'])['Time'].nunique()
		city_fail_df = city_fail.to_frame()
		city_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
		city_fail_df = city_fail_df.reset_index()
		city_fail_df = city_fail_df.sort_values(by='Count', ascending=False)
		city_fail_list = city_fail_df.index.tolist()
		city_list_count = len(city_fail_list)

		st.header('City Unsuccessful Access Count')
		city_count_slider = st.slider('City Count', max_value=city_list_count, value=5)
		st.table(city_fail_df.head(city_count_slider).set_index('City'))
	except:
		pass

	try:
		username_fail = failed_logs.groupby('User')['Time'].nunique()
		username_fail_df = username_fail.to_frame()
		username_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
		username_fail_df = username_fail_df.reset_index()
		username_fail_df = username_fail_df.sort_values(by='Count', ascending=False)
		username_fail_list = username_fail_df.index.tolist()
		username_list_count = len(username_fail_list)

		st.header('Username Unsuccessful Access Count')
		username_count_slider = st.slider('Username Count', max_value=username_list_count, value=5)
		st.table(username_fail_df.head(username_count_slider).set_index('User'))
	except:
		pass

	try:
		ip_fail = failed_logs.groupby('Source_IP')['Time'].nunique()
		ip_fail_df = ip_fail.to_frame()
		ip_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
		ip_fail_df = ip_fail_df.reset_index()
		ip_fail_df = ip_fail_df.sort_values(by='Count', ascending=False)
		ip_fail_list = ip_fail_df.index.tolist()
		ip_list_count = len(ip_fail_list)

		st.header('IP Unsuccessful Access Count')
		ip_count_slider = st.slider('IP Count', max_value=username_list_count, value=5)
		st.table(ip_fail_df.head(ip_count_slider).set_index('Source_IP'))
	except:
		pass

def servers_hit():
	auth_logs = db.auth_logs_to_df()
	auth_logs['Hour'] = auth_logs['Time'].str.split(':').str[0]
	auth_logs = auth_logs.sort_values(['Hour'], ascending=True)

	# Side Bar
	result = st.sidebar.button('Load Data')
	if result:
		search()

	# Jumpbox Data
	jump_boxes = []
	jump_boxes_options = (auth_logs['Box'].unique().tolist())
	for i in jump_boxes_options:
		jump_boxes.append(i)
	jump_boxes.sort()
	jump_boxes.insert(0, 'All')

	side_jumpbox = st.sidebar.selectbox('Servers', (jump_boxes))

	if side_jumpbox == 'All':
		failed_logs = auth_logs.loc[auth_logs['Access'] == 'Failed']
		pass_logs = auth_logs.loc[auth_logs['Access'] == 'Successful']

	else:
		for i in jump_boxes_options:
			if side_jumpbox == i:
				failed_logs = auth_logs.loc[auth_logs['Access'] == 'Failed']
				pass_logs = auth_logs.loc[auth_logs['Access'] == 'Successful']

				failed_logs = failed_logs.loc[auth_logs['Box'] == i]
				pass_logs = pass_logs.loc[auth_logs['Box'] == i]
			else:
				pass

	# Country
	country_boxes = []
	pass_country_options = (pass_logs['Country'].unique().tolist())
	fail_country_options = (failed_logs['Country'].unique().tolist())

	for i in pass_country_options:
		if i not in country_boxes:
			country_boxes.append(i)
	for i in fail_country_options:
		if i not in country_boxes:
			country_boxes.append(i)

	country_boxes.sort()
	country_count = len(country_boxes)
	country_boxes.insert(0, 'All')
	country_count = len(country_boxes) - 1
	country_text = 'Which Country ? Total = ' + str(country_count)
	side_country = st.sidebar.selectbox(country_text, (country_boxes))

	if side_country == 'All':
		pass

	else:
		for i in country_boxes:
			if side_country == i:
				failed_logs = failed_logs.loc[auth_logs['Country'] == i]
				pass_logs = pass_logs.loc[auth_logs['Country'] == i]
			else:
				pass

	# city
	city_boxes = []
	pass_city_options = (pass_logs['City'].unique().tolist())
	fail_city_options = (failed_logs['City'].unique().tolist())

	for i in pass_city_options:
		if i not in city_boxes:
			city_boxes.append(i)
	for i in fail_city_options:
		if i not in city_boxes:
			city_boxes.append(i)

	city_boxes.sort()
	city_boxes.insert(0, 'All')
	city_count = len(city_boxes) - 1
	city_text = 'Which City ? Total = ' + str(city_count)
	side_city = st.sidebar.selectbox(city_text, (city_boxes))

	if side_city == 'All':
		pass

	else:
		for i in city_boxes:
			if side_city == i:
				failed_logs = failed_logs.loc[auth_logs['City'] == i]
				pass_logs = pass_logs.loc[auth_logs['City'] == i]
			else:
				pass

		# Dates
	d = datetime.today() - timedelta(days=7)

	dates = []
	pass_date_options = (pass_logs['Date'].unique().tolist())
	fail_date_options = (failed_logs['Date'].unique().tolist())

	for i in pass_date_options:
		if i not in dates:
			dates.append(i)
	for i in fail_date_options:
		if i not in dates:
			dates.append(i)

	all_dates_check = st.sidebar.checkbox('All Dates')

	if all_dates_check:
		pass

	else:
		try:
			layout = st.sidebar.columns([2, 1])

			min_date = min(dates)
			year = min_date.split('/')[0]
			month = min_date.split('/')[1]
			date = min_date.split('/')[2]

			min_date_time = datetime(int(year), int(month), int(date))

			with layout[0]:
				start_date = st.date_input('Start Date:', max_value=datetime.today())  # omit "sidebar"
			with layout[0]:
				end_date = st.date_input('End Date:', value=(d), min_value=min_date_time,
										 max_value=datetime.today())  # omit "sidebar"

			new_start = str(start_date).replace('-', '/')
			new_end = str(end_date).replace('-', '/')
			pass_logs = pass_logs[(pass_logs['Date'] > new_end) & (pass_logs['Date'] <= new_start)]
			failed_logs = failed_logs[(failed_logs['Date'] > new_end) & (failed_logs['Date'] <= new_start)]
		except:
			pass
	st.sidebar.image('Images/Ned_Logo_Pictorial_T.png')
	st.header('Unsucessfull IP Servers Hit Count')

	sort_by = st.selectbox('Sort By',['Box Hit Count', 'Total Hits'])
	country_codes = db.grab_country_codes()

	if sort_by == 'Total Hits':
		try:
			all_boxes = list(set(failed_logs['Box'].tolist()))
			all_boxes.sort()
			all_ips = list(set(failed_logs['Source_IP'].tolist()))
			all_ips.sort()
			full_count_data = []
			for ip in stqdm(all_ips, desc='Analyzing All IPs For Server Hit Count'):
				boxes_hit_count = 0
				ip_df = failed_logs.loc[failed_logs['Source_IP'] == ip]

				with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
					response = reader.city(ip)
				city = response.city.name
				country = response.country.iso_code

				row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
				df_list = row.values.tolist()
				country = df_list[0][0]


				ip_info = {'IP': [ip]}
				ip_count_df = pd.DataFrame(ip_info)
				for box in all_boxes:
					box_df = ip_df.loc[ip_df['Box'] == box]
					count = len((box_df['Box'].tolist()))
					ip_count_df.insert(1, box, count, True)
					if count > 0:
						boxes_hit_count = boxes_hit_count + 1

				ip_count_df['Total Hits'] = ip_count_df.sum(axis=1)
				ip_count_df['Boxes Hit'] = boxes_hit_count
				ip_count_df.insert(1, 'Country', country, True)
				ip_count_df.insert(1, 'City', city, True)
				full_count_data.append(ip_count_df)

			box_hit_df = pd.concat(full_count_data, axis=0, ignore_index=True)
			box_hit_df_final = box_hit_df.sort_values(['Total Hits'], ascending=False)

			all_ips_count = len(list(set(failed_logs['Source_IP'].tolist())))
			ipserver_count_slider = st.slider('Server Hit Count', max_value=all_ips_count, value=5)
			st.table(box_hit_df_final.head(ipserver_count_slider).set_index('IP'))

		except:
			pass

	if sort_by == 'Box Hit Count':

		try:
			all_boxes = list(set(failed_logs['Box'].tolist()))
			all_boxes.sort()
			all_ips = list(set(failed_logs['Source_IP'].tolist()))
			all_ips.sort()
			full_count_data = []
			for ip in stqdm(all_ips, desc='Analyzing All IPs For Server Hit Count'):
				boxes_hit_count = 0
				ip_df = failed_logs.loc[failed_logs['Source_IP'] == ip]

				with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
					response = reader.city(ip)
				city = response.city.name
				country = response.country.iso_code

				row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
				df_list = row.values.tolist()
				country = df_list[0][0]

				ip_info = {'IP': [ip]}
				ip_count_df = pd.DataFrame(ip_info)
				for box in all_boxes:
					box_df = ip_df.loc[ip_df['Box'] == box]
					count = len((box_df['Box'].tolist()))
					ip_count_df.insert(1, box, count, True)
					if count > 0:
						boxes_hit_count = boxes_hit_count + 1

				ip_count_df['Total Hits'] = ip_count_df.sum(axis=1)
				ip_count_df['Boxes Hit'] = boxes_hit_count
				ip_count_df.insert(1, 'Country', country, True)
				ip_count_df.insert(1, 'City', city, True)
				full_count_data.append(ip_count_df)

			box_hit_df = pd.concat(full_count_data, axis=0, ignore_index=True)
			box_hit_df_final = box_hit_df.sort_values(['Boxes Hit', 'Total Hits'], ascending=False)

			all_ips_count = len(list(set(failed_logs['Source_IP'].tolist())))
			ipserver_count_slider = st.slider('Server Hit Count', max_value=all_ips_count, value=5)
			st.table(box_hit_df_final.head(ipserver_count_slider).set_index('IP'))
		except:
			pass

def search():
	db.log_pull()
	db.auth_log_to_db()
	auth_logs = db.auth_logs_to_df()
	auth_logs.sort_values(by=['Date_Time'], inplace=True, ascending=False)

def box_hit_data():
	  # sorts the df by first name column
	return(box_hit_df)