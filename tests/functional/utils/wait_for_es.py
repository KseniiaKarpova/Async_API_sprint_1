import time

from elasticsearch import Elasticsearch
from functional.settings import test_settings
import logging

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=f"http://{test_settings.es_host}:{test_settings.es_port}", verify_certs=False)
    logging.warning(f"{test_settings.es_host}")
    while True:
        if es_client.ping():
            break
        time.sleep(10)
