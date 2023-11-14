import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get('ES_HOST')
PORT = os.environ.get('ES_PORT')
URL = f"http://{HOST}:{PORT}"
