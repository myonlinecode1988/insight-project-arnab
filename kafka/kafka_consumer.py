from kafka import KafkaConsumer
import redis

redis_server = "localhost"
r = redis.StrictRedis(redis_server, port=6379, db=0)

consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='earliest',consumer_timeout_ms=10*1000)
consumer.subscribe(['my-topic'])

#writing to redis
for message in consumer:
    r.set(message.key,message.value)
    pass
