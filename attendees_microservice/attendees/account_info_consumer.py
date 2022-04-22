from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

# make sure to do djang.setup() before following because it sets up the database.
# Otherwise next command won't have data it needs to work

from attendees.models import AccountVO


# Declare a function to update the AccountVO object (ch, method, properties, body)
def update_AccountVO_object(ch, method, properties, body):
    print("  Received %r" % body)
    #   content = load the json in body
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]  # date when updated
    #   updated = convert updated_string from ISO string to datetime
    updated = datetime.fromisoformat(updated_string)
    #   if is_active:
    if is_active:
        new_values = {
            "first_name": first_name,
            "last_name": last_name,
            "updated": updated,
        }
        AccountVO.objects.update_or_create(
            email=email,
            defaults=new_values,
        )
        #       Use the update_or_create method of the AccountVO.objects QuerySet
        #           to update or create the AccountVO object
        print("Inside if_active block")
    else:
        #       Delete the AccountVO object with the specified email, if it exists
        AccountVO.objects.filter(email=email).delete()
        print("inside delete block within update_accountVO_object function")


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
while True:
    try:

        #           create the pika connection parameters
        parameters = pika.ConnectionParameters(host="rabbitmq")
        print("setting up pubsub")

        #           create a blocking connection with the parameters
        connection = pika.BlockingConnection(parameters)

        #           open a channel
        channel = connection.channel()
        print("connected to channel")

        #           declare a fanout exchange named "account_info"
        channel.exchange_declare(
            exchange="account_info", exchange_type="fanout"
        )

        #           declare a randomly-named queue
        result = channel.queue_declare(queue="", exclusive="True")

        #           get the queue name of the randomly-named queue
        queue_name = result.method.queue

        #           bind the queue to the "account_info" exchange
        channel.queue_bind(exchange="account_info", queue=queue_name)

        #           do a basic_consume for the queue name that calls
        #           function above
        #
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_AccountVO_object,
            auto_ack=True,
        )

        print("setup consumer")
        #           tell the channel to start consuming
        channel.start_consuming()

    except AMQPConnectionError:
        print("Could not connect to Rabbit MQ")
        time.sleep(2.0)
