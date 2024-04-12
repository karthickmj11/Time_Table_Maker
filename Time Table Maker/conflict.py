import configparser
import os
import re
from datetime import datetime, timedelta

def into_seconds(entry,sec):
    hours = int(entry.split(":")[0])
    minutes = int(entry.split(":")[1])
    seconds = int(entry.split(":")[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds+sec
    return total_seconds

def conf(a,h):
    li =[]
    fin = []
    for i in a:
        li.append(i[0])
    for i in range(len(li)):
        for j in range(i+1,len(li)):
            if (datetime.strptime(li[i],'%H:%M:%S') - datetime.strptime(li[j],'%H:%M:%S')).seconds < 39001:
                if h > (datetime.strptime(li[i],'%H:%M:%S') - datetime.strptime(li[j],'%H:%M:%S')).seconds:
                    fin.append((i,j,(datetime.strptime(li[i],'%H:%M:%S') - datetime.strptime(li[j],'%H:%M:%S')).seconds))
            else:
                if h > (datetime.strptime(li[j],'%H:%M:%S') - datetime.strptime(li[i],'%H:%M:%S')).seconds:
                    fin.append((i,j,(datetime.strptime(li[j],'%H:%M:%S') - datetime.strptime(li[i],'%H:%M:%S')).seconds))
    return fin

def conflict(path,head):
    with open(os.path.join(path,'Timetable.xml')) as file:
        l = file.readlines()
    f = open(os.path.join(path,'Log.xml'),'w')
      
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(),'patterns.ini'))
    s = {'Up':{},'Down':{}}
    s['Up'] = {key.upper()+'_1': [] for key in (config.get('data','stations')).split(',')}
    s['Down'] = {key.strip().upper()+'_2': [] for key in (config.get('data','stations')).split(',')}
    flag = 0
    ser=[]
    sum = 0
    
    plot_d ={}
    prev = ''
    for j,i in enumerate(l):
        a = re.search('NUMBER="([\d]+)" TRIP_ID="([^"]+)" SERVICE_ID="([\d]+)" DIRECTION="[\w]+" ENTRY_TIME="([^"]+)"',i)
        b = re.search('TOP="Stop_STA_([^"]+)" DWELLTIME="([\d]+)"',i)
        c = re.search('TOP="([^"]+)" RUNTIME="([\d]+)"',i)
        if a is not None:
            flag = 1
            
            trip = a.group(1)
            trip_id = a.group(2)
            service = a.group(3)
            entry = a.group(4)
            if j!=0 and prev !=a.group(3):
                plot_d[service] = {}
            prev = a.group(3)
            
            plot_d[service][trip_id] = {}
        if '</TRIP>' in i:
            flag = 0
            sum = 0
        if flag == 1 and b is not None:
            sum += int(b.group(2))
            sta = b.group(1).upper()
            if('</TRIP>' in l[j+1]):
                time = datetime.strptime(entry, '%H:%M:%S')
                updated_time = time + timedelta(seconds = int(sum))
                
                
                
    
                total_seconds = into_seconds(entry,sum)
                k = []
                k.append(updated_time.strftime('%H:%M:%S'))
                k.append(trip)
                k.append(trip_id)
                k.append(service)
                k.append(entry)
                if(sta[-1] == '1'):
                    s['Up'][sta].append(k)
                    plot_d[service][trip_id][sta[:-2]] = total_seconds
                elif(sta[-1] == '2'):
                    s['Down'][sta].append(k)
                    plot_d[service][trip_id][sta[:-2]] = total_seconds
                    
        if flag == 1 and c is not None:
            sum += int(c.group(2))
            time = datetime.strptime(entry, '%H:%M:%S')
            updated_time = time + timedelta(seconds = int(sum))
            total_seconds = into_seconds(entry,sum)
            k = []
            k.append(updated_time.strftime('%H:%M:%S'))
            k.append(trip)
            k.append(trip_id)
            k.append(service)
            k.append(entry)
            if(sta[-1] == '1'):
                s['Up'][sta].append(k)
                plot_d[service][trip_id][sta[:-2]] = total_seconds
            elif(sta[-1] == '2'):
                s['Down'][sta].append(k)
                plot_d[service][trip_id][sta[:-2]] = total_seconds
    conf_plot =[]
    for k in s.keys():
        cur_k = list(s[k].keys())
        for key,nk in enumerate(cur_k):
                pro = conf(s[k][nk],int(head))
                if pro is not None:
                    
                    for prob in pro:
                        tn = []
                        f.write(f'conflict in trip id : {s[k][nk][prob[0]][1]} with {s[k][nk][prob[1]][1]} at {nk} headway is {prob[2]}\n')
                        t1 = into_seconds(s[k][nk][prob[0]][0],0)
                        t2 = into_seconds(s[k][nk][prob[1]][0],0)
                        tn = [(nk,t1),(nk,t2)]
                        conf_plot.append(tn)
    return(plot_d,conf_plot)


