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
import sqlite3
from stqdm import stqdm



def add_server(box, ip, username, private_key, port):
    root = 'root' 
    try:
        conn = sqlite3.connect('Data/ned.db')
        c = conn.cursor()
        c.execute('INSERT INTO Box_Info(Box, IP, Username, Private_Key, Port) VALUES (?,?,?,?,?)',(box, ip, root, private_key, port))
        print(c.execute)
        conn.commit()
        c.close()
        conn.close()
        print('Box information inserted successfully into Boxes table')
    except:
        print('Failed to insert box information into Boxes table')
   
def auth_log_to_db():
    db = sqlite3.connect('Data/ned.db')
    df = pd.read_sql_query('SELECT * FROM Full_Log', db)
    full_log = df['Log'].tolist()

    auth_logs = pd.DataFrame(columns = ['Date_Time', 'Date', 'Time','Source_IP','Access','Box','User','By_Way', 'City', 'Country', 'Lat', 'Lon'])

    print('Creating Data Frame')
    time_bar = len(full_log)
    
    with alive_bar(time_bar) as bar:
        for x in stqdm(full_log, desc='Analyzing All Auth_Logs'):
            try:
                x = x.replace('  ', ' ')
            except:
                pass
            if 'CRON[208036]' in x:
                pass
            if 'sshd' in x:
                try:
                    if 'Accepted' in x:
                        if 'publickey' in x:
                            month = x.split(' ')[0]
                            num_month = strptime(month,'%b').tm_mon
                            day = int(x.split(' ')[1])
                            time = x.split(' ')[2]
                            hour = int(time.split(':')[0])
                            minute = int(time.split(':')[1])
                            second = int(time.split(':')[2])
                            dt = datetime.datetime(2021, num_month, day, hour, minute, second, tzinfo=pytz.UTC)

                            fmt = "%Y/%m/%d %H:%M:%S"
                            pacific = dt.astimezone(timezone('US/Pacific'))
                            date_time = pacific.strftime(fmt)
                            ip = x.split('from ')[1].split(' ')[0]
                            box = x.split(' ')[3]
                            user = x.split('for ')[1].split(' ')[0]

                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            lat = response.location.latitude
                            lon = response.location.longitude


                            new_row = {'Date_Time':date_time.split(' PDT-0700')[0],'Source_IP':ip, 'Access':'Successful','Box':box,'User':user,'By_Way':'Public_Key','City':city,'Country':country,'Lat':lat,'Lon':lon,'Date':date_time.split(' ')[0],'Time':date_time.split(' ')[1]}
                            auth_logs = auth_logs.append(new_row, ignore_index=True)


                        else:
                            month = x.split(' ')[0]
                            num_month = strptime(month,'%b').tm_mon
                            day = int(x.split(' ')[1])
                            time = x.split(' ')[2]
                            hour = int(time.split(':')[0])
                            minute = int(time.split(':')[1])
                            second = int(time.split(':')[2])
                            dt = datetime.datetime(2021, num_month, day, hour, minute, second, tzinfo=pytz.UTC)

                            fmt = "%Y/%m/%d %H:%M:%S"
                            pacific = dt.astimezone(timezone('US/Pacific'))
                            date_time = pacific.strftime(fmt)
                            ip = x.split('from ')[1].split(' ')[0]
                            box = x.split(' ')[3]
                            user = x.split('for ')[1].split(' ')[0]

                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            lat = response.location.latitude
                            lon = response.location.longitude

                            new_row = {'Date_Time':date_time.split(' PDT-0700')[0],'Source_IP':ip, 'Access':'Successful','Box':box,'User':user,'By_Way':'Password','City':city,'Country':country,'Lat':lat,'Lon':lon,'Date':date_time.split(' ')[0],'Time':date_time.split(' ')[1]}
                            auth_logs = auth_logs.append(new_row, ignore_index=True)
                except:
                    pass
                try:
                    if 'Failed' in x:
                        if 'invalid user' in x:
                            month = x.split(' ')[0]
                            num_month = strptime(month,'%b').tm_mon
                            day = int(x.split(' ')[1])
                            time = x.split(' ')[2]
                            hour = int(time.split(':')[0])
                            minute = int(time.split(':')[1])
                            second = int(time.split(':')[2])
                            dt = datetime.datetime(2021, num_month, day, hour, minute, second, tzinfo=pytz.UTC)


                            fmt = "%Y/%m/%d %H:%M:%S"
                            pacific = dt.astimezone(timezone('US/Pacific'))
                            date_time = pacific.strftime(fmt)
                            ip = x.split(' ')[12]
                            box = x.split(' ')[3]
                            user = x.split(' ')[10]


                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            lat = response.location.latitude
                            lon = response.location.longitude

                            new_row = {'Date_Time':date_time.split(' PDT-0700')[0],'Source_IP':ip, 'Access':'Failed','Box':box,'User':user,'By_Way': user,'City':city,'Country':country,'Lat':lat,'Lon':lon,'Date':date_time.split(' ')[0],'Time':date_time.split(' ')[1]}

                            auth_logs = auth_logs.append(new_row, ignore_index=True)
                        else:
                            month = x.split(' ')[0]
                            num_month = strptime(month,'%b').tm_mon
                            day = int(x.split(' ')[1])
                            time = x.split(' ')[2]
                            hour = int(time.split(':')[0])
                            minute = int(time.split(':')[1])
                            second = int(time.split(':')[2])
                            dt = datetime.datetime(2021, num_month, day, hour, minute, second, tzinfo=pytz.UTC)


                            fmt = "%Y/%m/%d %H:%M:%S"
                            pacific = dt.astimezone(timezone('US/Pacific'))
                            date_time = pacific.strftime(fmt)
                            ip = x.split(' ')[10]
                            box = x.split(' ')[3]
                            user = x.split(' ')[8]


                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            lat = response.location.latitude
                            lon = response.location.longitude

                            new_row = {'Date_Time':date_time.split(' PDT-0700')[0],'Source_IP':ip, 'Access':'Failed','Box':box,'User':user,'By_Way': user,'City':city,'Country':country,'Lat':lat,'Lon':lon,'Date':date_time.split(' ')[0],'Time':date_time.split(' ')[1]}

                            auth_logs = auth_logs.append(new_row, ignore_index=True)
                    else:
                        pass
                except:
                    pass
                else:
                    pass
            else:
                pass
            bar()

    print('Data Frames complete')
    auth_logs["City"].fillna('None', inplace = True)
    auth_logs.sort_values(by=['Date_Time'], inplace=True, ascending=False)

    conn = sqlite3.connect('Data/ned.db')
    c = conn.cursor()
    auth_logs.to_sql('Auth_Logs', conn, if_exists='replace', index = False)
    try:
        c.close
        conn.close()
        print('Database closed')
    except:
        print('Database not closed')    
    return auth_logs

def auth_logs_to_df():
    try:
        db = sqlite3.connect('Data/ned.db')
        df = pd.read_sql_query('SELECT * FROM Auth_Logs', db) 
        return df
        print('Box Information successfully')
    except:
        print('Failed to connect to the database')

def delete_server(server):
    try:
        delresult = '"'+server+'"'
        conn = sqlite3.connect('Data/ned.db')
        c = conn.cursor()
        c.execute('DELETE from Box_Info WHERE Box='+str(delresult))
        conn.commit()
        c.close()
        conn.close()
        return('Delete Successful')
    except:
        return('Delete Unsuccessful')

def db_log_add(full_logs):
    time_bar = len(full_logs)
    db = sqlite3.connect('Data/ned.db')
    with alive_bar(time_bar) as bar:
        for x in full_logs:
            cursor = db.cursor()
            cursor.execute('INSERT OR IGNORE INTO Full_Log(log) VALUES (?)',[x])
            db.commit()
            bar()

def grab_box_info():
    print('Loading Box Information')
    try:
        db = sqlite3.connect('Data/ned.db')
        df = pd.read_sql_query("SELECT * FROM Box_Info", db) 
        return df
        print('Box Information successfully')
    except:
        print('Failed to connect to the database')         
            
def log_pull():

    print('Starting Log Pull')
    
    boxes = grab_box_info()
    box_names = []
    full_logs = []
    
    for index, row in boxes.iterrows():
        box = str(row['Box'])
        box_names.append(box)
        print('Appended', box)
    
    for x in box_names:
        db = sqlite3.connect('Data/ned.db')
        cursor = db.cursor()
        searchresult = '"'+x+'"'
        result = cursor.execute('SELECT * from Box_Info WHERE Box='+str(searchresult))
        row = result.fetchone()

        box = str(row[0])
        ip = str(row[1])
        usname = str(row[2])
        p_key = str(row[3])
        box_port = int(row[4])
        print(box, ip, usname, p_key, box_port)

        save_name = 'Data/' + box +'.txt'

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            with pysftp.Connection(ip, username=usname, private_key=p_key, port=box_port, cnopts=cnopts) as sftp:
                with sftp.cd('.'):
                    sftp.get('/var/log/auth.log', save_name)         # get a remote file
                    print('Successfully SCP file from', box)
            with open(save_name, 'r') as f:
                log = [line.strip() for line in f]
                for a in log:
                    full_logs.append(a)
                    
                print('Created log for', box)
                if os.path.exists(save_name):
                      os.remove(save_name)
                else:
                    print('The file does not exist')
        except:
            st.error('Unsuccessfully connected to ' + x)
            print('Connection not made to', box)

    db_log_add(full_logs)        
    return full_logs
    
def server_connection_check(server):
    x = server
    
    try:
        db = sqlite3.connect('Data/ned.db')
        cursor = db.cursor()
        searchresult = '"'+x+'"'
        result = cursor.execute('SELECT * from Box_Info WHERE Box='+str(searchresult))
        row = result.fetchone()
        print(row)

        box = str(row[0])
        ip = str(row[1])
        usname = str(row[2])
        p_key = str(row[3])
        box_port = int(row[4])
        print(box, ip, usname, p_key, box_port)
        
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(ip, username=usname, private_key=p_key, port=box_port, cnopts=cnopts) as sftp:
            with sftp.cd('.'):
                return('Connection Successful')
                print('Connection Successful')

    except:
        return('Connection Unsuccessful')
        print('Connection Unsuccessful')
           
def update_server_info(change,location,server_name):
    conn = sqlite3.connect('Data/ned.db')
    c = conn.cursor()
    c.execute('UPDATE Box_Info SET '+ location + ' = ? WHERE Box = ?',(change,server_name))
    print(c.execute)
    conn.commit()
    c.close()
    conn.close()




