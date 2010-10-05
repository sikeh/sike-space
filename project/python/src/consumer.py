from amqplib import client_0_8 as amqp
import time
import os
import sys

exchange = 'exchange'
queue = sys.argv[1]

conn = amqp.Connection(host='dev.rabbitmq.com')
ch = conn.channel()

ch.exchange_declare(exchange=exchange, type="fanout", durable=False, auto_delete=True)

ch.queue_declare(queue=queue, durable=False, exclusive=False, auto_delete=True)
ch.queue_bind(queue=queue, exchange=exchange)

def callback(msg):
    delivery_tag = msg.delivery_info['delivery_tag']
    print "%s %s %s" % (msg.delivery_info['channel'], delivery_tag, msg.body)
    ch.basic_ack(delivery_tag = delivery_tag)

ch.basic_consume(callback=callback, queue=queue)

while True:
    ch.wait()


