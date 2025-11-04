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

    # Output data to stdout
    # For production, this would be replaced with writing to a database 
    # with a different datastorage option e.g. 'psql'
    logger.info("Trades created: {}".format(output))


if __name__=="__main__":
    input_filepath = "data/orders.ndjson"
    main(input_filepath)
