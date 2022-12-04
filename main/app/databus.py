from paho.mqtt import client as mqtt

from app.config import BROKER_HOST, BROKER_PORT, SERVER_FORMAT


class DataBus:
    def __init__(self, client_id, on_message):
        self.broker = BROKER_HOST
        self.port = BROKER_PORT
        self.client = mqtt.Client(client_id)
        self.client.loop_start()
        self.client.on_message = on_message
        self.client.connect(self.broker, self.port)

    def subscribe(self, topic: str) -> int:
        """
        Subscribe topic.

        Args:
            topic (str): instance topic.
        Returns:
            int: MQTT_ERR_SUCCESS
        """
        result, _ = self.client.subscribe(topic, 1)
        return result

    def publish(self, topic: str, msg: str):
        """
        Publish message in broker topic.

        Args:
            topic (str): instance topic
            msg (str): instance message
        """
        self.client.publish(topic, msg)
