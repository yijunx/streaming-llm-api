#!/usr/bin/env python
import pika
import sys


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

    user_id = sys.argv[1]
    message = " ".join(sys.argv[2:]) or "Hello World!"
    channel.basic_publish(exchange="direct_logs", routing_key=user_id, body=message)
    print(" [x] Sent %r:%r" % (user_id, message))
    connection.close()