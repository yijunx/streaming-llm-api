# gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 app.flask_socket:app

from flask_sock import Sock
from flask import Flask, render_template, request
import pika
from datetime import datetime

app = Flask(__name__)
sock = Sock(app)


channels = {}
connections = {}


@app.route("/")
def index():
    return render_template("index.html")


def the_callback_for_exchange(ws, queue_name, exchange, routing_key):
    # well the exchange way is exactly what we want..
    def callback(ch, method, properties, body):
        try:
            # maybe we can add some memory stuff...
            ws.send(body.decode("utf-8"))
            print(f"from X")
        except Exception as e:
            print("collected backend stuff from rabbit, but..")
            print("well we cannot send throught the websocket anymore")
            print(e)
            print("thus we close the channel")
            ch.queue_unbind(
                queue=queue_name, exchange=exchange, routing_key=routing_key
            )
            ch.close()

    return callback


@sock.route("/direct_exchange/<user_x>")
def ws_for_users_with_exchange_type_direct(ws, user_x):
    # message will be lost if there is no queue bind to it
    # this bind is at server side
    print(f"using X at {datetime.now()}")
    routing_key = user_x
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    exchange = "direct_logs"
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="direct")

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange="direct_logs", queue=queue_name, routing_key=routing_key
    )
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=the_callback_for_exchange(
            ws, queue_name, exchange, routing_key
        ),
        auto_ack=True,
    )
    channel.start_consuming()
