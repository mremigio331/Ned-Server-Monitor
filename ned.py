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
import sqlite3

from datetime import datetime, timedelta

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


    


