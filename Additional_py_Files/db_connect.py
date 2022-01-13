import streamlit as st
import os
import glob
import pandas as pd
import pysftp
from time import strptime
from pytz import timezone
from time import strptime
from datetime import *
import pytz
import geoip2.database
import pydeck as pdk
from alive_progress import alive_bar, config_handler
import numpy as np
import sqlite3
from stqdm import stqdm
from backports.zoneinfo import ZoneInfo


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
   
def auth_log_to_db(new_logs):
    full_log = new_logs

    auth_logs = pd.DataFrame(columns = ['Date_Time', 'Date', 'Time','Source_IP','Access','Box','User','By_Way', 'City', 'Country', 'Lat', 'Lon'])

    country_codes = grab_country_codes()
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
                            year = int(datetime.utcnow().year)
                            dt = datetime(year, num_month, day, hour, minute, second, tzinfo=pytz.UTC)
                            fmt = "%Y/%m/%d %H:%M:%S"
                            dt.astimezone(ZoneInfo('US/Pacific'))
                            date_time = dt.strftime(fmt)
                            ip = x.split('from ')[1].split(' ')[0]
                            box = x.split(' ')[3]
                            user = x.split('for ')[1].split(' ')[0]

                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            try:
                                row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
                                df_list = row.values.tolist()
                                country = df_list[0][0]
                            except:
                                pass
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
                            year = int(datetime.utcnow().year)
                            dt = datetime(year, num_month, day, hour, minute, second, tzinfo=pytz.UTC)

                            fmt = "%Y/%m/%d %H:%M:%S"
                            dt.astimezone(ZoneInfo('US/Pacific'))
                            date_time = dt.strftime(fmt)
                            ip = x.split('from ')[1].split(' ')[0]
                            box = x.split(' ')[3]
                            user = x.split('for ')[1].split(' ')[0]

                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            try:
                                row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
                                df_list = row.values.tolist()
                                country = df_list[0][0]
                            except:
                                pass
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
                            year = int(datetime.utcnow().year)
                            dt = datetime(year, num_month, day, hour, minute, second, tzinfo=pytz.UTC)


                            fmt = "%Y/%m/%d %H:%M:%S"
                            dt.astimezone(ZoneInfo('US/Pacific'))
                            date_time = dt.strftime(fmt)
                            ip = x.split(' ')[12]
                            box = x.split(' ')[3]
                            user = x.split(' ')[10]


                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            try:
                                row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
                                df_list = row.values.tolist()
                                country = df_list[0][0]
                            except:
                                pass
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
                            year = int(datetime.utcnow().year)
                            dt = datetime(year, num_month, day, hour, minute, second, tzinfo=pytz.UTC)


                            fmt = "%Y/%m/%d %H:%M:%S"
                            dt.astimezone(ZoneInfo('US/Pacific'))
                            date_time = dt.strftime(fmt)
                            ip = x.split(' ')[10]
                            box = x.split(' ')[3]
                            user = x.split(' ')[8]


                            with geoip2.database.Reader('Data/IP_Lookup_City.mmdb') as reader:
                                response = reader.city(ip)
                            city = response.city.name
                            country = response.country.iso_code
                            try:
                                row = (country_codes.loc[country_codes['Alpha_2_Code'] == country])
                                df_list = row.values.tolist()
                                country = df_list[0][0]
                            except:
                                pass
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
    auth_logs.to_sql('Auth_Logs', conn, if_exists='append', index = False)
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
        for x in stqdm(full_logs, desc='Adding full logs to database'):
            cursor = db.cursor()
            cursor.execute('INSERT OR IGNORE INTO Full_Log(log) VALUES (?)',[x])
            db.commit()
            bar()

def full_logs():
    try:
        db = sqlite3.connect('Data/ned.db')
        df = pd.read_sql_query('SELECT * FROM Full_Log', db)
        return df
        print('Successfully connected to database')
    except:
        print('Unsuccessfully connected to database')

def grab_box_info():
    print('Loading Box Information')
    try:
        db = sqlite3.connect('Data/ned.db')
        df = pd.read_sql_query("SELECT * FROM Box_Info", db) 
        return df
        print('Box Information successfully')
    except:
        print('Failed to connect to the database')         

def grab_country_codes():
    print('Loading Box Information')
    try:
        db = sqlite3.connect('Data/ned.db')
        df = pd.read_sql_query("SELECT * FROM Country_Codes", db) 
        return df
        print('Successfully collected country codes')
    except:
        print('Failed to connect to the database')
            
def log_pull():

    boxes = grab_box_info()
    box_names = []
    full_logs = []
    success_scp = []
    
    for index, row in boxes.iterrows():
        box = str(row['Box'])
        box_names.append(box)
        print('Appended', box)
    
    print('Starting Log Pull')
    for x in stqdm(box_names, desc='Starting Log Pull'):
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
                    message = 'Successfully SCP file from ' + box
                    print(message)
                    success_scp.append(box)

            with open(save_name, 'r') as f:
                log = [line.strip() for line in f]
                time_bar = len(log)
                with alive_bar(time_bar) as bar:
                    log_message = 'Adding logs from' + x
                    for a in stqdm(log, desc=log_message):
                        full_logs.append(a)
                        bar()
                    
                print('Created log for', box)
                if os.path.exists(save_name):
                      os.remove(save_name)
                else:
                    print('The file does not exist')
        except:
            st.error('Unsuccessfully connected to ' + x)
            print('Connection not made to', box)

    success_scp.sort()
    last = success_scp[-1]
    del success_scp[-1]
    success_scp.append('and ' + last + '.')
    message = 'Successfully SCP files from ' + ' , '.join(success_scp)
    st.success(message)

    return full_logs

def log_update():

    boxesdf = grab_box_info()
    boxes = []

    for index, row in boxesdf.iterrows():
        box = str(row['Box'])
        boxes.append(box)
    auth_logs = auth_logs_to_df()
    min_df = pd.DataFrame(columns = ['Box','Last'])
    
    for x in boxes:
        df = auth_logs[auth_logs.Box == x]
        last_pull = df['Date_Time'].max()
        new_row = {'Box':x,'Last':last_pull}
        print(new_row)
        min_df = min_df.append(new_row, ignore_index=True)
    
    min_df = min_df.set_index(['Box'])
    dt = 'Jan 1 1900 01:01:01'
    dtg = datetime.strptime(dt, '%b %d %Y %H:%M:%S')
    min_df['Last'] = min_df['Last'].fillna(dtg)
    min_df['Last'] = pd.to_datetime(min_df['Last']).dt.tz_localize(pytz.timezone('UTC'))


    print(min_df)
    
    logs = log_pull()
    
    updated_logs = []

    time_bar = len(logs)
    
    print('Searching For New Logs')
    with alive_bar(time_bar) as bar:
        for l in stqdm(logs, desc='Searching For New Logs'):
            try:
                l = l.replace('  ', ' ')
            except:
                pass
            try:
                month = l.split(' ')[0]
                day = l.split(' ')[1]
                year = str(datetime.now().year)
                time = l.split(' ')[2]
                dtg = (month + ' ' + day + ' ' + str(year) + ' ' + time)
                box = l.split(' ')[3]
                dtg = datetime.strptime(dtg, '%b %d %Y %H:%M:%S')
                dtg = dtg.replace(tzinfo=timezone.utc)
                for b in boxes:
                    if box == b:
                        last_pull = min_df.loc[b][0]
                        if last_pull < dtg:
                            updated_logs.append(l)
                        else:
                            pass
                    else:
                        pass
            except:
                pass
                #print(l)
            bar()   

    db_log_add(updated_logs)
    new_auth_logs = auth_log_to_db(updated_logs)
    index = new_auth_logs.index
    number_of_rows = len(index)
    print(str(number_of_rows) + ' logs added to Ned data')
    st.success(str(number_of_rows) + ' logs added to Ned data')
    
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

def ned_settings_grab():
    pass

def ned_settings_update():
    pass
           
def update_server_info(change,location,server_name):
    conn = sqlite3.connect('Data/ned.db')
    c = conn.cursor()
    c.execute('UPDATE Box_Info SET '+ location + ' = ? WHERE Box = ?',(change,server_name))
    print(c.execute)
    conn.commit()
    c.close()
    conn.close()




