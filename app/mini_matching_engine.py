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
        input_stream = self.datasource.load(self.input_source)

        while input_stream:
            order = input_stream.popleft()
            self.process(order)

        return self.datastorage.output_stream()
    
    def process(self, order):
        if order.type == "create":
            self.order_book.add_order(order)
        elif order.type == "amend":
            self.order_book.amend_order(order)
        elif order.type == "cancel":
            self.order_book.cancel_order(order)
        else:
            logger.error("Order type not recognised.")