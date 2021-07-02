from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

class kafkaclient(object):
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers

    def send(self, topic, message, key=None):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, value_serializer=lambda m: json.dumps(m).encode('ascii'))
        future = producer.send(topic, value=message, key=key)
        code = 'ok'
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError as e:
            print(e)
            code = 'fail'
        finally:
            producer.close()
            return code