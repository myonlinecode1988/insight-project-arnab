###########################################################
# This is the bash script to submit streaming.py to spark #
###########################################################

/usr/local/spark/bin/spark-submit --master spark://ec2-54-214-202-16.us-west-2.compute.amazonaws.com:7077  --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.0 streaming.py

