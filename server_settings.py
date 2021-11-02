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
import db_connect as db
from datetime import datetime, timedelta

def server_page():

	st.title('Server Settings')
	server_settings_selection = st.selectbox('Server Settings', ['Add Server','Delete Server','Edit Server','Server Status'])


	if server_settings_selection == 'Add Server':
	    add_server()
	if server_settings_selection == 'Delete Server':
	    delete_server()
	if server_settings_selection == 'Edit Server':
	    edit_server()
	if server_settings_selection == 'Server Status':
	    server_status()

	st.sidebar.image('Images/Ned_Logo_Emblem_T.png')


def add_server():

	st.header('Add Server')
	box = st.text_input('Box Name')
	ip = st.text_input('IP Address')
	username = st.text_input('Username By Default = root')
	private_key = st.text_input('Private Key Location')
	port = st.text_input('Port')

	save = st.button('Add Server')
	
	if save:
		try:
			result = db.add_server(box, ip, username, private_key, port)
			st.success('Server Added To Database')
		except:
			st.error('Server Unsuccessful Added To Database')
		try:
			connection_check = db.server_connection_check(box)
			if connection_check == 'Connection Successful':
				st.success('Server Connection Successful')
				st.balloons()

			if connection_check == 'Connection Unsuccessful':
				st.error('Server Connection Unsuccessful')
		except:
			st.error('Something is fucked up')

def delete_server():
	st.header('Delete Server')

	server_info = db.grab_box_info()
	servers = []
	server_options = (server_info['Box'].unique().tolist())
	for i in server_options:
	    servers.append(i)
	servers.sort()


	server_selection = st.selectbox('Server', (servers))

	delete = st.button('Delete Server')

	if delete:

		try:
			server_delete = db.delete_server(server_selection)
			if server_delete == 'Delete Successful':
				st.success('Server Successfully Deleted')
			if server_delete == 'Delete Unsuccessful':
				st.error('Server Unsuccessfully Deleted')
		except:
			st.error('Something is fucked up')
	
def edit_server():
	st.header('Edit Server Info')
	server_info = db.grab_box_info()
	server_info_s = server_info.set_index('Box')
	server_info_s['IP'] = server_info_s['IP'].astype(str)
	server_info_s['Port'] = server_info_s['Port'].astype(str)

	servers = []
	server_options = (server_info['Box'].unique().tolist())
	for i in server_options:
	    servers.append(i)
	servers.sort()


	server_selection = st.selectbox('Server', (servers))

	for i in servers:
		if server_selection == i:
			server_pick = i
 
	new_server = st.text_input('Current Server Name is: ' + server_pick)
	change_server = st.checkbox('Update Server Name')

	current_ip = server_info_s.loc[server_pick]['IP']
	new_ip = st.text_input(('Current IP Address is: ' + current_ip))
	change_ip = st.checkbox('Update IP Address')
	
	current_username = server_info_s.loc[server_pick]['Username']
	new_username = st.text_input(('Current Username is: '+ current_username))
	change_username = st.checkbox('Update Username')
	
	current_key = server_info_s.loc[server_pick]['Private_Key'] 
	new_key = st.text_input(('Current SSH Key is: ' + current_key))
	change_key = st.checkbox('Update SSH Key Location')
	
	current_port = server_info_s.loc[server_pick]['Port']
	new_port = st.text_input(('Current Port is: ' + current_port))
	change_port = st.checkbox('Update Port')

	new_save = st.button('Update Server')

	if new_save:
		if change_ip:
			try:
				db.update_server_info(new_ip,'IP',server_pick)
				st.success('IP Updated')
				try:
					connection_check = db.server_connection_check(server_pick)
					if connection_check == 'Connection Successful':
						st.success('Server Connection Successful')
					if connection_check == 'Connection Unsuccessful':
						st.error('Server Connection Unsuccessful')
				except:
					st.error('Something is fucked up')
			except:
				st.error('Unsuccessful IP Update')
		if change_username:
			try:
				db.update_server_info(new_username,'Username',server_pick)
				st.success('Username Updated')
			except:
				st.error('Unsuccessful Username Update')
		if change_key:
			try:
				db.update_server_info(new_key,'Private_Key',server_pick)
				st.success('SSH Key Updated')
			except:
				st.error('Unsuccessful SSH Key Update')
		if change_port:
			try:
				db.update_server_info(new_port,'Port',server_pick)
				st.success('Port Updated')
			except:
				st.error('Unsuccessful Port Update')
		if change_server:
			try:
				db.update_server_info(new_server,'Box',server_pick)
				st.success('Server Name Updated')
			except:
				st.error('Unsuccessful Server Name Update')
	
def server_status():
	st.header('Server Status')

	server_info = db.grab_box_info()
	server_info_s = server_info.set_index('Box')
	server_info_s['IP'] = server_info_s['IP'].astype(str)
	server_info_s['Port'] = server_info_s['Port'].astype(str)

	servers = []
	server_options = (server_info['Box'].unique().tolist())
	for i in server_options:
	    servers.append(i)
	servers.sort()


	server_selection = st.selectbox('Server', (servers))

	status = st.button('Server Status')

	if status:
		try:
			connection_check = db.server_connection_check(server_selection)
			if connection_check == 'Connection Successful':
				st.success('Server Connection Successful')
			if connection_check == 'Connection Unsuccessful':
				st.error('Server Connection Unsuccessful')
		except:
			st.error('Something is fucked up')



