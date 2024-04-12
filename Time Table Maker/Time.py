
import re
from numpy import delete
import pandas as pd
from datetime import datetime, timedelta
import math
import configparser
import os
from tkinter import messagebox

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'patterns.ini'))
config.optionxform = str
station_list = config.get('data','stations')
stations = [item.strip() for item in station_list.split(',')]

global dwell
global services
d = {key.upper(): value for key, value in config['Dictionary'].items()}
pattern = {key.upper(): value for key, value in config['Links'].items()}

d = {}
pattern = {}
for key, value in config.items('Dictionary'):
    d[key.upper()] = value.split(',')


for key, value in config.items('Links'):
    q=[]
    for i in value.split(','):
        q.append(i.strip()+'\n')
    pattern[key.upper()] = q

config_dwell = configparser.ConfigParser()
config_dwell.read(os.path.join(os.getcwd(), 'Dwell.ini'))
dwell = {key.upper(): value for key, value in config_dwell['Dwell'].items()}

def Update_Dwell():
    config_dwell.read(os.path.join(os.getcwd(), 'Dwell.ini'))
    dwell = {key.upper(): value for key, value in config_dwell['Dwell'].items()}
    return dwell

#d = {}
#pattern = {}

#df = pd.read_excel(os.path.join(os.getcwd(), 'R1_R2_Extn_CLGT_WHTM_Full.xlsx'),sheet_name='Sheet2')
#df['Pat'] = df['Departure'] +'-'+ df['Arrival']
#df = df.set_index(['Pat'])

config_mode = configparser.ConfigParser()
config_mode.read(os.path.join(os.getcwd(), 'modes.ini'))

data = {}
for section in config_mode.sections():
    data[section] = {}
    for option in config_mode.options(section):
        data[section][option] = config_mode.get(section, option)

df = pd.DataFrame(data).T

def pat_mak(a):
    l = a.split('_')
    if(len(l)==9):
        return l[0]+'_'+'_'.join(l[5:])+'_'+'_'.join(l[1:5])
    elif(len(l)==5):
        return l[0]+'_'+'_'.join(l[3:])+'_'+'_'.join(l[1:3])
    else:
        if(l[1]=='STL' or l[1]=='COD'):
            return l[0]+'_'+'_'.join(l[5:])+'_'+'_'.join(l[1:5])
        else:
            return l[0]+'_'+'_'.join(l[3:])+'_'+'_'.join(l[1:3])

def dir(a):
    l = a.split('-')
    if(stations.index(l[0])<stations.index(l[1])):
        return 'RIGHT'
    else:
        return 'LEFT'
def stop(a):
   l = a.split('_')
   f = [i for i in l if i in stations ]
   return f[0]+'-'+f[1]

services = []
def Run(dwell,mul,out,ind,ind_1,idx,mode,ser,entry_time,tr,file1,status):

   
   if(status == "RUN"):
       
       try:
            time = datetime.strptime(entry_time, '%H:%M:%S')
       except ValueError:
             messagebox.showerror('ERROR','Enter Correct Time Format')
       services.append(ser)
       for i in range(0,mul):
            if(i%2==0):
                if(i==0):
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="" NEXT_NUMBER="{str(tr+1)}">\n')
                elif(i>0 and i<mul-1):                                                 
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="{str(tr+1)}">\n')
                else:                                                              
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="">\n')
                for item in pattern[idx.upper()]:
                    temp = re.search('TOP="LL_Stop_([^"]+)"',item)
                    temp1 = re.search('TOP="Stop_([^"]+)"',item)
                    if temp1 is not None:
                       sto = temp1.group(1)[4:].upper()
                       time = datetime.strptime(entry_time, '%H:%M:%S')
                       updated_time = time + timedelta(seconds = int(dwell[sto]))
                       entry_time = updated_time.strftime('%H:%M:%S')
                       item = item.split(' ')[0]+''+item.split(' ')[1]+' DWELLTIME="'+str(dwell[sto])+'" '+''.join(item.split(' ')[2:])
                    if temp is not None:
                        st = stop(temp.group(1))
                        if(st.split('-')[0]!=st.split('-')[1]):
                            time = datetime.strptime(entry_time, '%H:%M:%S')
                            updated_time = time + timedelta(seconds=math.ceil(float(df.loc[st, mode.lower()])))
                            entry_time = updated_time.strftime('%H:%M:%S')
                            item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(math.ceil(float(df.loc[st, mode.lower()])))+'" '+''.join(item.split(' ')[2:])
                        else:
                            time = datetime.strptime(entry_time, '%H:%M:%S')
                            updated_time = time + timedelta(seconds=60) 
                            entry_time = updated_time.strftime('%H:%M:%S')
                            item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(60)+'" '+''.join(item.split(' ')[2:])
                        item = item.replace('LINK','RUN ')
                    item = item.replace('STOPTOP','STOP TOP')
                    out.append(item)
                out.append('</TRIP>\n')
            
            else:
               if(i==0):
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="" NEXT_NUMBER="{str(tr+1)}">\n')
               elif(i>0 and i<mul-1):                                                 
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="{str(tr+1)}">\n')
               else:                                                              
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="">\n')
               try:
                   for item in pattern[pat_mak(idx.upper())]:
                         temp = re.search('TOP="LL_Stop_([^"]+)"',item)
                         temp1 = re.search('TOP="Stop_([^"]+)"',item)
                         if temp1 is not None:
                             sto = temp1.group(1)[4:].upper()
                             time = datetime.strptime(entry_time, '%H:%M:%S')
                             updated_time = time ++ timedelta(seconds = int(dwell[sto]))
                             entry_time = updated_time.strftime('%H:%M:%S')
                             item = item.split(' ')[0]+''+item.split(' ')[1]+' DWELLTIME="'+str(dwell[sto])+'" '+''.join(item.split(' ')[2:])
                         if temp is not None:
                             st = stop(temp.group(1))
                             if(st.split('-')[0]!=st.split('-')[1]):
                                 time = datetime.strptime(entry_time, '%H:%M:%S')
                                 updated_time = time + timedelta(seconds=math.ceil(float(df.loc[st, mode.lower()])))
                                 entry_time = updated_time.strftime('%H:%M:%S')
                                 item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(math.ceil(float(df.loc[st, mode.lower()])))+'" '+''.join(item.split(' ')[2:])
                             else:
                                 time = datetime.strptime(entry_time, '%H:%M:%S')
                                 updated_time = time + timedelta(seconds=60)
                                 entry_time = updated_time.strftime('%H:%M:%S')
                                 item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(60)+'" '+''.join(item.split(' ')[2:])
                             item = item.replace('LINK','RUN ')
                         item = item.replace('STOPTOP','STOP TOP')
                         out.append(item)
                   out.append('</TRIP>\n')
               except KeyError:
                   messagebox.showerror('KeyError',F'{pat_mak(idx.upper())} pattern does not exist')
                   break
        
            tr+=1
       messagebox.showinfo('INFO',f'Trips generated for Service ID : {ser}')
       
   if(status == 'FINISH'):
       fi = file1+'\Timetable.xml'
       fil = open(fi,'w+')
       

       try:
            time = datetime.strptime(entry_time, '%H:%M:%S')
       except ValueError:
             messagebox.showerror('ERROR','Enter Correct Time Format')

       try:
           value = d[ind]
       except KeyError:
           messagebox.showerror('Key Error',"Please Enter Appropiate Stations")
       fil.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
       fil.write('<ROOT>\n')
       fil.write('   <Versions>\n')
       fil.write('      <ID Name="OGT-G" Version="OGT-G-05.64"></ID>\n')
       fil.write('      <ID Name="OGT-ATS-INTERFACE" Version="3.0"></ID>\n')
       fil.write('      <ID Name="ODPT_APPLICATION_AREA" Version="BLR_1190"></ID></Versions>\n')
       fil.write('   <TITLE>Schedule file</TITLE>\n')
       fil.write('   <SCHEDULE NAME="L1_WKDY_BYPH_MYRD_27_01_23" COMMENT="" SERVICE="">\n')
       fil.write('      <TRIPS>\n')
       for i in out:
            fil.write(i)
            fil.flush()
       fil.write('      </TRIPS>\n')
       fil.write('   </SCHEDULE>\n')
       fil.write('</ROOT>\n')
       fil.close()
       messagebox.showinfo('INFO','Time Table generated Successfully...')
