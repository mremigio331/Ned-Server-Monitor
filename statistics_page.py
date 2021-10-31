import streamlit as st
import os
import glob
import pandas as pd
import pysftp
from time import strptime
from datetime import datetime
from pytz import timezone
from time import strptime
from datetime import datetime
from dateutil import tz
import datetime
import pytz
import geoip2.database
import pydeck as pdk
from alive_progress import alive_bar, config_handler
from dateutil.relativedelta import relativedelta
import numpy as np
from pandas_datareader import data
import db_connect
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import altair as alt


def statistics():
	st.title('Statistics')
	auth_logs = db_connect.auth_logs_to_df()
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
	    pass_logs = auth_logs.loc[auth_logs['Access'] == 'Sucessful']

	else: 
	    for i in jump_boxes_options:
	        if side_jumpbox == i:
	            failed_logs = auth_logs.loc[auth_logs['Access'] == 'Failed']
	            pass_logs = auth_logs.loc[auth_logs['Access'] == 'Sucessful']

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

	layout = st.sidebar.beta_columns([2, 1])

	with layout[0]: 
	    start_date = st.date_input('Start Date:',max_value=datetime.today()) # omit "sidebar"
	with layout[0]: 
	    end_date = st.date_input('End Date:',value=(d),max_value=datetime.today()) # omit "sidebar"

	new_start = str(start_date).replace('-','/')
	new_end = str(end_date).replace('-','/')



	pass_logs = pass_logs[(pass_logs['Date'] > new_end) & (pass_logs['Date'] <= new_start)]
	failed_logs = failed_logs[(failed_logs['Date'] > new_end) & (failed_logs['Date'] <= new_start)]

	st.sidebar.image('Images/Ned_Logo_Emblem_T.png')

	dates = []
	all_dates = (auth_logs['Date'].unique().tolist())
	for i in all_dates:
	    dates.append(i)
	dates.sort()

	st.set_option('deprecation.showPyplotGlobalUse', False)
	st.header('Sucessful Access')
	new = pass_logs.groupby('Date')['Time'].nunique()
	st.line_chart(new)

	st.set_option('deprecation.showPyplotGlobalUse', False)
	st.header('Unsucessful Access')
	newf = failed_logs.groupby('Date')['Time'].nunique()
	#new['Time'] = new['Time'].astype(int)
	plotnew = newf.to_frame().reset_index()

	#st.dataframe(plotnew)
	st.line_chart(newf)
	alt.Chart(plotnew).mark_line(point=True).encode(x='Time',y='Date')
	country_fail = failed_logs.groupby('Country')['Time'].nunique()
	country_fail_df = country_fail.to_frame()
	country_fail_df.rename({'Time':'Count'}, axis=1, inplace=True)
	country_fail_df = country_fail_df.reset_index()

	st.header('Country Unsucessful Access Count')
	st.table(country_fail_df)

