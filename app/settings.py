import logging
import os
import sys


RABBIT_MQ_URL = os.getenv("RABBIT_MQ_URL", default="amqp://guest:guest@localhost/")

logging.basicConfig(
    format="%(asctime)s:%(msecs)03d %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
