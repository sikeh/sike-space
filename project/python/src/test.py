from amqplib import client_0_8 as amqp
import time
import os

regular_sleep = 10

nightjobs_sleep_base = 10
nightjobs_sleep_threshold = 60

nightjobs_sleep = nightjobs_sleep_base

lock = 'C://lock.txt'

queue='test_queue'
exchange='test_exchange'

conn = amqp.Connection(host='dev.rabbitmq.com')
ch = conn.channel()

ch.exchange_declare(exchange=exchange, type="fanout", durable=False, auto_delete=False)

ch.queue_declare(queue=queue, durable=False, exclusive=False, auto_delete=False)
ch.queue_bind(queue=queue, exchange=exchange)

while True:
    if os.path.exists(lock):
        print 'sleep %s' % str(nightjobs_sleep)
        time.sleep(nightjobs_sleep)
        nightjobs_sleep =  nightjobs_sleep*2
        if nightjobs_sleep > nightjobs_sleep_threshold:
            nightjobs_sleep = nightjobs_sleep_base
        print 'wake up'
    else:
        msg = ch.basic_get()
        if msg:
            pass
        else:
            print 'sleep %s' % str(regular_sleep)
            time.sleep(regular_sleep)
            print 'wake up'


