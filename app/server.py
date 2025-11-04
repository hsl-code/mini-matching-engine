"""Application/Microservices boilerplate code.

The process method is called.
"""
from mini_matching_engine import MatchingEngine


def main(input_filepath):
    engine = MatchingEngine(
                    input_filepath,
                    datasource='file',
                    datastorage='file'
                    )
    output = engine.process_stream()
    print(output)


if __name__=="__main__":
    input_filepath = "../data/orders.ndjson"
    main(input_filepath)
