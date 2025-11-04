"""Application/Microservices boilerplate code.

The process method is called.
"""
from logger import getLogger
logger = getLogger(__name__)

from mini_matching_engine import MatchingEngine


def main(input_filepath):
    engine = MatchingEngine(
                    input_filepath,
                    datasource='file',
                    datastorage='dict_array'
                    )
    logger.info("Process stream data.")
    output = engine.process_stream()


if __name__=="__main__":
    input_filepath = "data/orders.ndjson"
    main(input_filepath)
