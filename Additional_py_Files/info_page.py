import streamlit as st

def info():
	st.sidebar.image('Images/Ned_Logo_Emblem_T.png')
	
	st.title('Information')

	st.header('Steps To Connecting To Server')
	st.subheader('Creating SSH Keys')
	st.text('You will first need to create SSH Keys for your server. After the keys are connected to the server, place the SSH keys in the Keys directory within the code')

	st.subheader('SSH_Config Settings')
	st.text('In order for the code to work properly you will need to change a setting in your ssh_config file.')
	st.text('To access the file, connect to your server.')
	st.text('Navigate to the sshd_config file which is located in /etc/ssh/sshd_config')
	st.text('Unhash the Loglevel and change from INFO to VERBOSE')
	st.text('It is also recommended to change your SSH port')

	st.subheader('Connecting Ned To Your Server')
	st.text('To connect Ned to your server, open the Server Settings page and enter in your server details. If you need to change any settings you can do so by selecting Edit Server in the Server Settings Page')
	st.text('To confirm you have access to your server you can select Server Status in the Server Settings page.')

	st.subheader('Grabbing Information from your server')
	st.text('To get the authentication logs from your server navigate to the Home Page and select Load Data. Below the maps notifications will appear to indicate if proper connections were made.')