###########################################################
# This is the bash script to submit batch.py to spark #
###########################################################

/usr/local/spark/bin/spark-submit --master spark://ec2-54-214-202-16.us-west-2.compute.amazonaws.com:7077 --packages mysql:mysql-connector-java:5.1.38  batch.py

