import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


while True:
    try:
        # Create a function that will process the message when it arrives
        # ch is channel, #method is info regarding message delivery
        # properties are user-defined properties on the message, like key value, maybe routing key?
        def process_approval(ch, method, properties, body):
            print("  Received %r" % body)
            message = json.loads(body)
            name = message.get("presenter_name")
            presentation = message["title"]
            email = message["presenter_email"]
            send_mail(
                "Your presentation has been accepted",
                name
                + ", we're happy to tell you that your presentation "
                + presentation
                + " has been accepted",
                "admin@conference.go",
                [email],
            )

        def process_rejection(ch, method, properties, body):
            print("  Received %r" % body)
            message = json.loads(body)
            name = message["presenter_name"]
            presentation = message["title"]
            email = message["presenter_email"]
            send_mail(
                "Your presentation has been rejected",
                name
                + ", we're sorry to tell you that your presentation "
                + presentation
                + " has been rejected",
                "admin@conference.go",
                [email],
            )

        # The following is code that needs to apply to both functions! some can be repeated to specify a certain queue, and some cannot!!!
        # BEWARE!!!!!!
        # DO NOT REPEAT parameters, connection or channel!!!!!
        # DO NOT REPEAT channel.basic_consume either! It is an infinite loop!

        # Set the hostname that we'll connect to
        parameters = pika.ConnectionParameters(host="rabbitmq")

        # create a connection to RabbitMQ
        connection = pika.BlockingConnection(parameters)

        # Open a channel to RabbitMQ
        channel = connection.channel()

        # Checks if queue exists, assigns if not. Can do this more than once!
        channel.queue_declare(queue="presentation_approvals")

        # Configure the consumer to call the process_approval
        # function when a message arrives. Can set this more than once!
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )

        # Create a queue if it does not exist
        channel.queue_declare(queue="presentation_rejections")

        # Configure the consumer to call the process_approval
        # function when a message arrives
        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        # Tell RabbitMQ that you're ready to receive messages
        # Infinite loop!!!!!
        channel.start_consuming()

    except AMQPConnectionError:
        print("Could not connect to Rabbit MQ")
        time.sleep(2.0)
