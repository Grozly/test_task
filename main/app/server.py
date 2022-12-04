import socket
import threading
import logging
from queue import Queue

from app.client import Client
from app.databus import DataBus
from app.config import (
    SERVER_PORT,
    SERVER_ADDR,
    SERVER_FORMAT,
)


logger = logging.getLogger(__name__)
logger.setLevel(level="INFO")


SUBSCRIBE_COMMAND = "subscribe"
POLL_COMMAND = "poll"

HELLO_MESSAGE = (
    f"\nPlease enter command [{SUBSCRIBE_COMMAND} <some_topic>, {POLL_COMMAND}] \n"
    f">>> Description <<<\n"
    f"{SUBSCRIBE_COMMAND} <some_topic> - subscription to the topic \n"
    f"{POLL_COMMAND} - receive a message \n"
)


def on_message(client, userdata, message):
    server.queue_messages.put({message.topic: message.payload.decode(SERVER_FORMAT)})


class Server:
    def __init__(self):
        self.port = SERVER_PORT
        self.clients = set()
        self.recive_clients = set()
        self.clients_lock = threading.Lock()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.databus = DataBus("server", on_message)
        self.queue_messages = Queue()

    def run(self):
        self.server.bind(SERVER_ADDR)
        self.server.listen(5)
        logger.warning("Running Server on PORT " + str(self.port))
        while True:
            self.__start_session()

    def __start_session(self):
        """
        Start a new session for the client.
        """
        session = self.server.accept()
        client = Client(session)
        threading._start_new_thread(self.__client_handle, (client,))

    def __client_handle(self, client: Client):
        """
        Сlient handler.

        Args:
            client (Client): instance client
        """
        logger.warning(f"{client.address} connected!")
        self.clients.add(client.connection)
        client.send(HELLO_MESSAGE)

        try:
            connected = True
            while connected:
                msg = client.connection.recv(1024).decode(SERVER_FORMAT)
                is_poll_command = msg == f"{POLL_COMMAND}\r\n"

                if not msg:
                    break

                if (
                    not is_poll_command
                    and not client.have_poll_command
                    and client.subscribed == 0
                ):
                    msg = self.__formatted_message(msg)
                    self.databus.publish(client.current_topic, msg)

                if msg.startswith(SUBSCRIBE_COMMAND):
                    _, topic = msg.split(" ")
                    topic = self.__formatted_message(topic)
                    result = self.databus.subscribe(topic)
                    client.set_subscribed(result, topic)

                if is_poll_command:
                    client.set_poll()
                    self.recive_clients.add(client)
                    with self.clients_lock:
                        threading.Thread(target=self.__worker, daemon=True).start()

        except UnicodeDecodeError:
            connected = False
        finally:
            with self.clients_lock:
                self.clients.remove(client.connection)

            client.connection.close()
            logger.warning(f"{client.address} disconnected!")

    def __formatted_message(self, msg: str) -> str:
        """
        Formatted message.

        Args:
            msg (str): instance message
        Returns:
            str: formatted message
        """
        return msg.strip()

    def __worker(self):
        """
        Worker for send messages to clients.
        """
        while self.queue_messages != 0:
            item = self.queue_messages.get()
            [c.send(item) for c in self.recive_clients]
            self.queue_messages.task_done()
        self.queue_messages.join()


server = Server()
