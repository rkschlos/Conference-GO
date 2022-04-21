from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from .models import AccountVO

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

#make sure to do djang.setup() before following because it sets up the database.
# Otherwise next command won't have data it needs to work

from attendees.models import AccountVO:

# Declare a function to update the AccountVO object (ch, method, properties, body)
def update_AccountVO_object(ch, method, properties, body):
#   content = load the json in body
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"] # date when updated
    #   updated = convert updated_string from ISO string to datetime
    updated = datetime.fromisoformat(updated_string)
#   if is_active:
    if is_active:
        AccountVO.objects.update_or_create()
#       Use the update_or_create method of the AccountVO.objects QuerySet
#           to update or create the AccountVO object
    else:
#       Delete the AccountVO object with the specified email, if it exists
        AccountVO.objects.filter(id = email)


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
# infinite loop
#   try
#       create the pika connection parameters
#       create a blocking connection with the parameters
#       open a channel
#       declare a fanout exchange named "account_info"
#       declare a randomly-named queue
#       get the queue name of the randomly-named queue
#       bind the queue to the "account_info" exchange
#       do a basic_consume for the queue name that calls
#           function above
#       tell the channel to start consuming
#   except AMQPConnectionError
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds