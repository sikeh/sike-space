#!/usr/bin/env python
# -*- coding:utf-8 -*-

# http://www.rainsts.net/article.asp?id=1040

from sys import exit
from amqplib import client_0_8 as amqp
from time import sleep
from multiprocessing import Process, current_process

host = 'dev.rabbitmq.com'
userid = "guest"
password = "guest"
queue = "sike_queue"
exchange = "sike_exchange"
routing_key = "sike_key"

def consumer(queue, exchange, type, routing_key):
    with amqp.Connection(host=host, userid = userid, password = password) as conn:
        with conn.channel() as chan:

            chan.queue_declare(queue = queue, auto_delete = False)
            chan.exchange_declare(exchange = exchange, type = type, auto_delete = False)
            chan.queue_bind(queue = queue, exchange = exchange, routing_key = routing_key)

#            while True:
#                msg = chan.basic_get(queue)
#                if msg:
#                    print current_process().pid, msg.body
#                    chan.basic_ack(msg.delivery_tag)
#                else:
#                    sleep(1)

            def cb(msg):
                print current_process().pid, msg.body
                if msg.body == "cancel":
                    chan.basic_cancel("x")
                    print "Consumer Exit!"
                    exit(0)

            chan.basic_consume(queue = queue, no_ack = True, callback = cb, consumer_tag = "x")
            while True: chan.wait()

def publisher(exchange, routing_key):
    with amqp.Connection(host=host, userid = userid, password = password) as conn:
        with conn.channel() as chan:
            x = 0
            while True:
                msg = amqp.Message("message {0}".format(x) if x < 10 else "cancel")
                chan.basic_publish(msg, exchange = exchange, routing_key = routing_key)

                if x >= 10:
                    print "Publisher Exit!"
                    exit(0)
                else:
                    x += 1
                    sleep(1)

if __name__ == "__main__":
    pub = Process(target = publisher, args = [exchange, routing_key])
    pub.start()

    con = Process(target = consumer, args = [queue, exchange, "direct", routing_key])
    con.start()

    pub.join()
    con.join()
