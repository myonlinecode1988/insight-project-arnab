import redis
import numpy as np
import pandas as pd
import time
import datetime
import os
import pandas as pd
redis_server = "localhost"
r = redis.StrictRedis(redis_server, port=6379, db=0)

county_list=["ALAMEDA",\
"ALPINE",\
"AMADOR",\
"BUTTE",\
"CALAVERAS",\
"COLUSA",\
"CONTRA COSTA",\
"DEL NORTE",\
"EL DORADO",\
"FRESNO",\
"GLENN",\
"HUMBOLDT",\
"IMPERIAL",\
"INYO",\
"KERN",\
"KINGS",\
"LAKE",\
"LASSEN",\
"LOS ANGELES",\
"MADERA",\
"MARIN",\
"MARIPOSA",\
"MENDOCINO",\
"MERCED",\
"MODOC",\
"MONO",\
"MONTEREY",\
"NAPA",\
"NEVADA",\
"ORANGE",\
"PLACER",\
"PLUMAS",\
"RIVERSIDE",\
"SACRAMENTO",\
"SAN BENITO",\
"SAN BERNARDINO",\
"SAN DIEGO",\
"SAN FRANCISCO",\
"SAN JOAQUIN",\
"SAN LUIS OBISPO",\
"SAN MATEO",\
"SANTA BARBARA",\
"SANTA CLARA",\
"SANTA CRUZ",\
"SHASTA",\
"SIERRA",\
"SISKIYOU",\
"SOLANO",\
"SONOMA",\
"STANISLAUS",\
"SUTTER",\
"TEHAMA",\
"TRINITY",\
"TULARE",\
"TUOLUMNE",\
"VENTURA",\
"YOLO",\
"YUBA"]

t0=time.mktime(time.strptime("30 Apr 18 0 0 0", "%d %b %y %H %M %S"))
time_list=[]
location_list=[]
count_list=[]
for sec in range(0,20):
    time_list=[]
    location_list=[]
    count_list=[]
    for county in county_list:
        curr_time=t0+sec
        startT=time.strftime("%b %d %Y %H:%M:%S",time.localtime(curr_time))
        time_list.append(startT)
        location_list.append(county)
        count_list.append(r.get(startT+','+county))
    print len(time_list),len(location_list),len(count_list)
    df = pd.DataFrame({'startT':time_list,'Location':location_list,'Count':count_list})
    df_json=df.to_json(orient='index')
    print df_json
