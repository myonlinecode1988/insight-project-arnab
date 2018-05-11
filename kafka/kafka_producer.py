import random
import sys
import datetime
import numpy as np
from kafka import KafkaProducer
import time
import os
import boto

# configuration file
#import config


def main():
    producer = KafkaProducer(bootstrap_servers = 'ec2-52-35-181-6.us-west-2.compute.amazonaws.com')
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')
    
    bucket_name = "call-data-record-s3"
    folder_name = "data/"
    for num in range(0,20): 
    	file_name = "cdr_"+str(num)+".csv"
    	conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
    	
    	bucket = conn.get_bucket(bucket_name)
    	key = bucket.get_key(folder_name + file_name)
    	t0=time.time()
    	
    	data = key.get_contents_as_string()
    	data_split=data.split('\n')
    	data_split=data_split[:-1]
    	data_split=data_split[1:]
    	for msg in data_split:
	    #splited=msg.split(',')
	    #message_info = '{"SourcePN": "%s", "DestPN": "%s", "Location": "%s","StartT": "%s","EndT": "%s","Type": "%s", "Company" : "%s"}' \
	    #    % (splited[0], splited[1], splited[2],splited[3],splited[4],splited[5],splited[6])
            #producer.send('cdr-data', message_info.encode('utf-8'))
            producer.send('cdr-data', msg.encode('utf-8'))
    	t1=time.time()
    	print 'access time=',t1-t0
    	# block until all async messages are sent
    	producer.flush()
    	
    	# configure multiple retries
    	producer = KafkaProducer(retries=5)

    return


if __name__ == '__main__':
    main()

