from flask import Flask, render_template,request,jsonify, json
from flask_socketio import SocketIO, emit                                       
import time                                                                     
import eventlet
import redis
import numpy as np
import pandas as pd
import time
import os
from flaskext.mysql import MySQL
from datetime import datetime


#List of counties
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


eventlet.monkey_patch()
app = Flask(__name__)                                                           
app.config['SECRET_KEY'] = 'secret!'


# Amazon Aurora MySQL  connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'asarkar'
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'default')
app.config['MYSQL_DATABASE_DB'] = 'cdr_records'
app.config['MYSQL_DATABASE_HOST'] = 'cdr-arnab.cgtyrrrwpzic.us-west-2.rds.amazonaws.com'
mysql.init_app(app)                                           
socketio = SocketIO(app)                                                        
thread = None                                                                   

# redis connection
redis_server = "localhost"
r = redis.StrictRedis(redis_server, port=6379, db=0)
t0=time.mktime(time.strptime("30 Apr 18 0 0 0", "%d %b %y %H %M %S"))

# redis dbase query every second
def background_thread():                                                        
    while True:
	
        for sec in range(0,20):
	    # remove for loop for production run
    	    time_list=[]
    	    location_list=[]
    	    count_list=[]
	    
            # read from redis,convert to json and send it to client side
    	    for county in county_list:
            	curr_time=t0+sec
            	startT=time.strftime("%b %d %Y %H:%M:%S",time.localtime(curr_time))
            	time_list.append(startT)
            	location_list.append(county)
            	count_list.append(r.get(startT+','+county))
    	    df = pd.DataFrame({'startT':time_list,'Location':location_list,'Count':count_list})
    	    df_json=df.to_json(orient='index')
            socketio.emit('test', df_json,json=True) 
    	    time.sleep(1)                                                           


@socketio.on('connect')                                                         
def connect():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=background_thread)       


@app.route('/', methods=['GET','POST'])                                                                 
def index():
    # Default plot . I don't want empty area on screen
    value_att = ['AT&T', 20357, 20380, 20613, 20931, 20747, 20563, 20501, 20420, 20541]
    value_sprint = ['Sprint', 6201, 6226, 6130, 6214, 6285, 6028, 6128, 6151, 6126]
    value_tmobile = ['T-mobile', 12429, 12158, 12496, 12430, 12381, 12075, 12247, 12282, 12467]
    value_verizon = ['Verizon', 12312, 12159, 12238, 12354, 12400, 12422, 12176, 12177, 12341]
    value_timestamp = ['Apr 30 2018 00:00', 'Apr 30 2018 00:01', 'Apr 30 2018 00:02', 'Apr 30 2018 00:03', 'Apr 30 2018 00:04', 'Apr 30 2018 00:05', 'Apr 30 2018 00:06', 'Apr 30 2018 00:07', 'Apr 30 2018 00:08']
    
    if request.method == 'POST':
        startT = request.form['startT']
        endT = request.form['endT']
        #Time is of format e.g. 04/30/2018 12:00
        #Convert the time format e.g. Apr 30 2018 00:00
        startT=datetime.strptime(startT, '%d:%m:%Y %H:%M').strftime("%b %d %Y %H:%M")
        endT=datetime.strptime(endT, '%d:%m:%Y %H:%M').strftime("%b %d %Y %H:%M")
        
        #Send query to Amamzon Aurora
        query='SELECT * FROM bi_table WHERE StartMin BETWEEN \''+startT+'\' AND \''+endT+'\' AND TYPE=\'CALL\''
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        
        #Send data that is compatible to c3.js
        value_timestamp= map(lambda x: str(x[0]) , data)
        value_att = map(lambda x: int(x[2]) , data)
        value_att=['AT&T']+value_att
        value_sprint = map(lambda x: int(x[3]) , data)
        value_sprint=['Sprint']+value_sprint
        value_tmobile = map(lambda x: int(x[4]) , data)
        value_tmobile=['T-mobile']+value_tmobile
        value_verizon = map(lambda x: int(x[5]) , data)
        value_verizon=['Verizon']+value_verizon
        print value_att
    return render_template('index.html',value_att=value_att,value_sprint=value_sprint,\
    value_tmobile=value_tmobile,value_verizon=value_verizon,value_timestamp=value_timestamp)        


if __name__ == '__main__':                                                      
    socketio.run(app, debug=True)
