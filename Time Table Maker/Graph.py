import configparser
import os
from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import conflict

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(),'patterns.ini'))

stop = [i for i in (config.get('data','stations')).split(',')]
ti = np.arange(0,82800,1200)




colors = [
   
    '#33A8FF',
    '#FFD133',
    '#FF336B',
    '#A8FF33',
    '#FF33A8',
    '#6BFF33',
    '#33FF33',
    '#FF33A8',
    '#33FFA8',
    '#A8FF33',
    '#FFD133',
    '#FF33EC',
    '#FF5733',
    '#A832DD',
    '#33FFA8',
    '#FF33EC',
    '#33FF6B',
    '#336BFF',
    'b',
    'g',
    'c',
    'm',
    'y',
    'k',
    'w',
    
]


def Show(path,head):
    i=0
    custom = []
    plot_d = conflict.conflict(path,head)[0]
    conf_plot = conflict.conflict(path,head)[1]
    for key,value in plot_d.items():
        prev = []
        for k,plots in value.items(): 
            x_values = []
            y_values = []
            for index, (stops, tim) in enumerate(plots.items()):
                x_values.append(tim)
                y_values.append(stop[::-1].index(stops))  
                if index == len(plots.items())-1:
                    prev =[]
                    prev.append(tim)
                    prev.append(stop[::-1].index(stops))
                if(len(prev)!=0 and prev[1] == stop[::-1].index(stops)):
                    x=[]
                    y=[]
                    x.append(prev[0])
                    x.append(tim)
                    y.append(prev[1])
                    y.append(stop[::-1].index(stops))
                    plt.plot(x,y,color=colors[i%25])
            plt.plot(x_values, y_values, marker='1',color=colors[i%25],label=f'Service {key}')
        custom.append(plt.Line2D([0], [0], color=colors[i%25], lw=2, label=f'Service {key}'))
        i+=1
    for po in conf_plot:
        xv = []
        yv = []
        for pa in po:
            yv.append(stop[::-1].index(pa[0][:len(pa[0])-2]))
            xv.append(int(pa[1]))
        plt.plot(xv, yv, marker='s',color='red')
    
            
    
    x_labels = [str(timedelta(seconds=int(i))) for i in ti]
    
    plt.yticks(range(len(stop)), stop[::-1])
    
    plt.xticks(ti, x_labels, rotation=90, ha='right')
    #mpldatacursor.datacursor()
    
    plt.xlabel('Time')
    plt.ylabel('Stations')
    plt.title('Time Table Graph View')
    plt.legend(handles=custom)
    plt.grid(True, axis='x', linestyle='--', linewidth=0.2)
    plt.grid(True, axis='y', linestyle='--', linewidth=0.2)
    plt.tight_layout()
    plt.show()
