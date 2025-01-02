import pika, json

from dotenv import load_dotenv
from borrows.etcd_gateway import get_etcd_key

load_dotenv()

MESSAGE_BROKER_URL = get_etcd_key('MESSAGE_BROKER_URL')

params = pika.URLParameters(MESSAGE_BROKER_URL)


def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='borrow', body=json.dumps(body), properties=properties)
    print('Message sent')

    channel.close()
    connection.close()