import logging
import sys

logging.basicConfig(
        handlers=[logging.StreamHandler(stream=sys.stdout)],
        level=logging.DEBUG
)