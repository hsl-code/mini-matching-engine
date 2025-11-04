"""Service implementation. Implementation of Processor lives here.
"""
from logger import getLogger
logger = getLogger(__name__)


from domain.order_book import OrderBook

from data_source.datasource_manager import DataSourceManager
from storage.data_storage_manager import DataStorageManager


class MatchingEngine:
    def __init__(self, 
                 input_source,
                 datasource='kafka', 
                 datastorage='psql') -> None:
        self.input_source = input_source
        self.datasource = DataSourceManager(datasource)
        self.datastorage = DataStorageManager(datastorage)
        self.order_book = OrderBook()

    def process_stream(self):
        logger.info("Loading input source into input stream.")
        input_stream = self.datasource.load(self.input_source)
        print(input_stream)

        logger.info("Commence stream data processing.")
        while input_stream:
            # Pop the first order
            order = input_stream.pop(0)
            print(order)
            self.process(order)

        return self.datastorage.output_stream()
    
    def process(self, order):
        if order.type == "create":
            logger.info("Add order {} to book.".format(order.order_id))
            self.order_book.add_order(order)
        elif order.type == "amend":
            logger.info("Amend order {}.".format(order.order_id))
            self.order_book.amend_order(order)
        elif order.type == "cancel":
            logger.info("Cancel order {}.".format(order.order_id))
            self.order_book.cancel_order(order)
        else:
            logger.error("Order type not recognised.")

        logger.info("Get trades as array.")
        return self.order_book.get_trades()