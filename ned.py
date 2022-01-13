import streamlit as st
import sys
sys.path.append('Additional_py_Files/')
import home_page as home
import statistics_page as stats 
import server_settings as server
import info_page as info

st.set_page_config(page_title='Ned', page_icon='Images/Ned_Logo_Pictorial_T.png', layout='wide', initial_sidebar_state='auto')
page = st.sidebar.selectbox('Page', ['Home','Info','Server Settings','Statistics'])
st.title("Ned Server Monitoring System")


if page == 'Home':
    home.home()
if page == 'Info':
    info.info()
if page == 'Server Settings':
    server.server_page()
if page == 'Statistics':
    stats.statistics()