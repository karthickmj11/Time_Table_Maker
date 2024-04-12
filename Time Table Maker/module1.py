
import re
from typing import Pattern
import pandas as pd
from datetime import datetime, timedelta
import math
import configparser
import os
from tkinter import messagebox

config = configparser.ConfigParser()
config.read('patterns.ini')
station_list = config.get('data','stations')
stations = [item.strip() for item in station_list.split(',')]

#d = {key.upper(): value for key, value in config['Dictionary'].items()}

config_dwell = configparser.ConfigParser()
config_dwell.read('Dwell.ini')
dwell = {key.upper(): value for key, value in config_dwell['Dwell'].items()}


d = {}
pattern = {}

df = pd.read_excel(r'C:\Users\491497\Downloads\R1_R2_Extn_CLGT_WHTM_Full.xlsx',sheet_name='Sheet2')
df['Pat'] = df['Departure'] +'-'+ df['Arrival']
df = df.set_index(['Pat'])
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

def sta(a):
    l = a.split('_')
    f = [i for i in l if i in stations ]
    return ''.join(f)

def input_file(a):
    a = r'C:\Users\491497\Desktop\Patterns_101.XML'
    flag=0
    p=[]
    gr = ''
    with open(a) as file:
        l = file.readlines()

    for i in l:
        a = re.search('NAME="([^"]+)"',i)
        if a is not None:
            flag = 1
            gr = a.group(1)
            if('PATTERN' in a.group(1)):
                key  = stop(a.group(1))
            else:
                continue
            if key not in d.keys():
                d[key] = [a.group(1)]
            else:
                d[key].append(a.group(1))
            
            
        else:
            if '</TRIPSTOPS>' in i:
                pattern[gr] = p
                p=[]
                continue
            if flag == 1:
                p.append(i)
    return d

def Run(mul,out,ind,ind_1,idx,mode,ser,entry_time,tr,file1,status):

   
   if(status == "RUN"):
       


       for i in range(0,mul+1):
            if(i%2==0):
                if(i==0):
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="" NEXT_NUMBER="{str(tr+1)}">\n')
                elif(i>0 and i<mul):                                                 
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="{str(tr+1)}">\n')
                else:                                                              
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="">\n')
                for item in pattern[d[ind][idx]]:
                    temp = re.search('TOP="LL_Stop_([^"]+)"',item)
                    temp1 = re.search('TOP="Stop_([^"]+)"',item)
                    if temp1 is not None:
                       sto = sta(temp1.group(1))
                       time = datetime.strptime(entry_time, '%H:%M:%S')
                       updated_time = time ++ timedelta(seconds = int(dwell[sto]))
                       entry_time = updated_time.strftime('%H:%M:%S')
                       item = item.split(' ')[0]+''+item.split(' ')[1]+' DWELLTIME="'+str(dwell[sto])+'" '+''.join(item.split(' ')[2:])
                    if temp is not None:
                        st = stop(temp.group(1))
                        if(st.split('-')[0]!=st.split('-')[1]):
                            time = datetime.strptime(entry_time, '%H:%M:%S')
                            updated_time = time + timedelta(seconds=math.ceil(df.at[st,mode]))
                            entry_time = updated_time.strftime('%H:%M:%S')
                            item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(math.ceil(df.at[st,mode]))+'" '+''.join(item.split(' ')[2:])
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
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="" NEXT_NUMBER="{str(tr+1)}">\n')
               elif(i>0 and i<mul):                                                 
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="{str(tr+1)}">\n')
               else:                                                              
                   out.append(f'<TRIP NUMBER="{str(tr)}" TRIP_ID="{str(tr).zfill(4)}" SERVICE_ID="{ser}" DIRECTION="{dir(ind_1)}" ENTRY_TIME="{entry_time}" DISTANCE="17998" TRAIN_CLASS="ANY" MISSION_TYPE="Passenger" RUNNING_MODE="Regulated" CREW_ID="" NEXT_CREW_ID="" NEXT_CREW_ID_LOCATION="" ROLLINGSTOCK_ID="" PREVIOUS_NUMBER="{str(tr-1)}" NEXT_NUMBER="">\n')
               for item in pattern[d[ind_1][idx]]:
                   temp = re.search('TOP="LL_Stop_([^"]+)"',item)
                   temp1 = re.search('TOP="Stop_([^"]+)"',item)
                   if temp1 is not None:
                       sto = sta(temp1.group(1))
                       time = datetime.strptime(entry_time, '%H:%M:%S')
                       updated_time = time ++ timedelta(seconds = int(dwell[sto]))
                       entry_time = updated_time.strftime('%H:%M:%S')
                       item = item.split(' ')[0]+''+item.split(' ')[1]+' DWELLTIME="'+str(dwell[sto])+'" '+''.join(item.split(' ')[2:])
                   if temp is not None:
                       st = stop(temp.group(1))
                       if(st.split('-')[0]!=st.split('-')[1]):
                           time = datetime.strptime(entry_time, '%H:%M:%S')
                           updated_time = time + timedelta(seconds=math.ceil(df.at[st,mode]))
                           entry_time = updated_time.strftime('%H:%M:%S')
                           item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(math.ceil(df.at[st,mode]))+'" '+''.join(item.split(' ')[2:])
                       else:
                           time = datetime.strptime(entry_time, '%H:%M:%S')
                           updated_time = time + timedelta(seconds=60)
                           entry_time = updated_time.strftime('%H:%M:%S')
                           item = item.split(' ')[0]+item.split(' ')[1]+' RUNTIME="'+str(60)+'" '+''.join(item.split(' ')[2:])
                       item = item.replace('LINK','RUN ')
                   item = item.replace('STOPTOP','STOP TOP')
                   out.append(item)
               out.append('</TRIP>\n')
            tr+=1
       
   if(status == 'FINISH'):
       #try:
       #    os.remove(fi)
       #except FileNotFoundError:
       #    messagebox.showinfo("ERROR", f"File '{fi}' not found. But No Problem")
       #except Exception as e:
       #    messagebox.showinfo(f"An error occurred while deleting the file: {e}")
       fi = file1+'\Timetable.xml'
       fil = open(fi,'w+')
       

       try:
            time = datetime.strptime(entry_time, '%H:%M:%S')
       except ValueError:
             messagebox.showerror('ERROR','Enter Correct Time Format')

       try:
           value = d[ind]
       except KeyError:
           messagebox.showerror('Key Error',"Please Enter Appropiate  Stations")
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
#Tight running profile
