[![Ring Map](https://github.com/myonlinecode1988/insight-project-arnab/blob/master/ring_map.png)]()


## Contents

1. [Introduction](README.md#introduction)
2. [Project Details](README.md#project-details)
3. [Pipeline](README.md#pipeline)
4. [Conclusion and Future Work](README.md#conclusion-and-future-work)

[Slides](http://bit.ly/2rBhiaD)
[Video](https://youtu.be/FUlDEAeGJZ8)


### Introduction
A call detail record is a log of incoming and outgoing calls. 
The USA sends about 6 billion texts per day and makes about 1.2 billion calls per day. All this data stream in as a log called Call Detail Record containing information like source phone number, destination phone number, start time, end time, product category, the telecom operator that it's calling etc. This project tries to simulate CDR analytics providing a streaming analytics engine that shows live call volume on a county level and a batch process that aggregates call volume across different telephone operators. About ~6k records streams in which simulates about 500 million calls and texts per day.

This is an existing business problem with a lot of data companies providing support to telecom operators. For e.g. Teradata works with Verizon to provide an analytics platform
for CDR.

### Project 
The CDR data is stored in S3. There are esentially two pipelines one for streaming and one for batch. The Kafka producers injest data at about ~6k records per second , followed by Spark Structured Streaming which reads data from the Kafka source. After necessary transformations it writes data on Kafka source which in turns writes data on Redis.
The flask app queries the Redis database every second and passes a json via websockets to the client side app that renders in the front end heat-map of california.

The batch process consists of reading data from S3 and processing is sprark batch job.
The output is used to quantify relative call volume between different telecom operator
showed in a stacked area plot.


### Pipeline
[![Pipeline#1](https://github.com/myonlinecode1988/insight-project-arnab/blob/master/pipeline.jpg)]()


### Conclusion and Future Work
A full-stack implementation of lambda architecture was performed in a period of three weeks. Although Spark Streaming gives a good performance; I would like the test it against other technologies like Flink. The dashboard should be made more informative showing a z-score based streaming information.


