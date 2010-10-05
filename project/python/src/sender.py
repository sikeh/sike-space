from amqplib import client_0_8 as amqp
import time
import os

exchange = 'exchange'
queue = 'queue'
routing_key = ''

message = 'it works'

conn = amqp.Connection(host='dev.rabbitmq.com')
ch = conn.channel()

ch.exchange_declare(exchange=exchange, type="fanout", durable=False, auto_delete=True)

msg = amqp.Message(message)
msg.properties["content_type"] = "text/plain"
msg.properties["delivery_mode"] = 2

ch.basic_publish(exchange=exchange, routing_key=routing_key, msg=msg)

ch.close()
conn.close()




