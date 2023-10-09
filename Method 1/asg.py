import pandas as pd 
import glob 
from math import cos, sin, asin, sqrt, radians
from timeit import default_timer as timer  
import os

def filename():
    index=1
    filename=os.path.join("matched", str(index) + '.csv')
    while glob.glob(filename):
        index+=1
        filename=os.path.join("matched", str(index) + '.csv')
    return filename
    
def haversine(lat1,lat2,long1,long2):
    R=6371 # Average radius of earth (Great circle distance)
    
    dlong =radians(long2 - long1)
    dlat = radians(lat2 - lat1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c=2*asin(sqrt(a))
    return c * R
    
start_time = timer()

df = pd.read_csv('people.csv')
dd = pd.read_csv('ppv.csv')
list=[]

for i in range(len(df)):
    
    nearppv=0
    lat1=df.values[i][1]
    lat2=dd.values[0][1]
    long1=df.values[i][2]
    long2=dd.values[0][2]
    nearlen=haversine(lat1,lat2,long1,long2)

    for j in range(len(dd)):
        lat1=df.values[i][1]
        lat2=dd.values[j][1]
        long1=df.values[i][2]
        long2=dd.values[j][2] 
        length=haversine(lat1,lat2,long1,long2)

        if length < nearlen:
            nearppv=j
            nearlen=length

    list.append([i,nearppv,nearlen])

matched=pd.DataFrame(list,columns=["People","PPV","Haversine distance"])
matched.to_csv(filename(),index=False)

end_time = timer()

totaltime=pd.DataFrame({'Performance':[end_time-start_time]})
totaltime.to_csv('performance.csv',mode='a',header=False,index=False)



