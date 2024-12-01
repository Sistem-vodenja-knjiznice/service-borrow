import pika, json, os
from dotenv import load_dotenv

load_dotenv()

MESSAGE_BROKER_URL = os.getenv('MESSAGE_BROKER_URL')

params = pika.URLParameters(MESSAGE_BROKER_URL)


def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='borrow', body=json.dumps(body), properties=properties)
    print('Message sent')

    channel.close()
    connection.close()