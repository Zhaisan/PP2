import pika
import time

def callback(ch, method, properties, body):
    print("Received: {}".format(body)) # message .... 4 sec
    time.sleep(body.count(b'.'))
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='example1')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='example1',on_message_callback=callback)

channel.start_consuming()