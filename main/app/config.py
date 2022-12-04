import os
from dotenv import load_dotenv


load_dotenv()


BROKER_HOST = os.getenv("BROKER_HOST")
BROKER_PORT = int(os.getenv("BROKER_PORT"))

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SERVER_FORMAT = os.getenv("SERVER_FORMAT")
SERVER_ADDR = (
    SERVER_HOST,
    SERVER_PORT,
)
