import os
import boto
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql import functions
import MySQLdb
from pyspark.sql.types import *


def get_dataframe(rdd_obj):
    """onvert RDD obj to DataFrame"""
    rdd = rdd_obj.map(lambda x: x.split(','))
    header = rdd.first()
    df = rdd.filter(lambda row: row != header).toDF(header)
    return df


def get_schema():
    """create schema for empty dataframe"""
    field = [StructField("StartMin", StringType(), True),\
    StructField('Type', StringType(), True),\
    StructField('ATT', StringType(), True),\
    StructField('Sprint', StringType(), True),\
    StructField('Tmobile', StringType(), True),\
    StructField('Verizon', StringType(), True)]
    schema = StructType(field)
    return schema


def main():
    # get MySQL password and keys
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')
    mysql_password = os.getenv('MYSQL_PASSWORD', 'default')

    # set spark context and reading from Amazon buckets
    sc = SparkContext(appName="Market-Share")
    spark = SparkSession(sc)
    sqlContext = SQLContext(sc)
    
    # processing data for five days
    for minute in range(0,432000,60):
        for second in range(0,60):
            file_name = "cdr_"+str(minute+second)+".csv"
            out_RDD = sc.textFile('s3a://call-data-record-s3/data/'+file_name)

            # read 60s worth of RDD and merge it formerge_RDD
            if (second == 0):
                formerge_RDD=out_RDD
            else:
                formerge_RDD = sc.union([formerge_RDD,out_RDD])

        #convert RDD obj to DataFrame
        outDF = get_dataframe(formerge_RDD)

        #remove second field from time stamp
        udf_remove_second = functions.udf(lambda x:x[:-3],StringType())
        df=outDF.withColumn('StartMin',udf_remove_second('StartT'))

        #remove unnecessary columns
        df = df.drop('Location','StartT','SourcePN','DestPN','EndT')
        CompanyDF=df.groupBy("StartMin","Type").pivot("Company").agg(functions.count('Type'))

        #apply new schema because spark cannot handle delimiting special characters
        df = df.drop('Location','StartT','SourcePN','DestPN','EndT')
        oldColumns=CompanyDF.schema.names
        newColumns = get_schema().names
        CompanyDF = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], \
        newColumns[idx]), xrange(len(oldColumns)), CompanyDF)
        
        #write on Amazon Aurora MySQL
        CompanyDF.write.format('jdbc').options(
        url='jdbc:mysql://cdr-arnab.cgtyrrrwpzic.us-west-2.rds.amazonaws.com:3306/cdr_records',
        driver='com.mysql.jdbc.Driver',
        dbtable='bi_table',
        user='asarkar',
        password=mysql_password).mode('append').save()


    sc.stop()


if __name__ == '__main__':
    main()
