from app.databus import DataBus
from app.config import SERVER_FORMAT


class Client:
    def __init__(self, session):
        self.connection = session[0]
        self.address = session[1]
        self.current_topic = None
        self.subscribed = 1
        self.have_poll_command = False

    def send(self, msg: str):
        """
        Send message for client.

        Args:
            msg (str): instance message
        """
        self.__send_raw(str(msg) + "\r\n")

    def __send_raw(self, msg):
        self.connection.send(str(msg).encode(SERVER_FORMAT))

    def set_subscribed(self, result: int, topic: str):
        """
        Set subscribed client.

        Args:
            result (int): subscribe status
            topic (str): instance topic
        """
        self.subscribed = result
        self.current_topic = topic

    def set_poll(self):
        """
        Set client have poll command.
        """
        self.have_poll_command = True
