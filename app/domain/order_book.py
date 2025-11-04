from logger import getLogger
logger = getLogger(__name__)


from collections import OrderedDict



class OrderBook:
    def __init__(self) -> None:
        """Order Book class

        buys - dict with buys with price as keys
        self.buys = {price: OrderedDict({order_id: order_obj})}  # O(1) deletion

        sells - dict with sells with price as keys
        self.buys = {price: OrderedDict({order_id: order_obj})}  # O(1) deletion

        orders - dict with all orders with order_id as keys
        trades - dict containing output trades
        """
        self.buys = OrderedDict()
        self.sells = OrderedDict()
        self.orders = OrderedDict()
        self.trades = OrderedDict()

    def add_order(self, order):
        """Add an order to the book and attempt to match it.
    
        If the order crosses with existing orders, execute trades.
        Any remaining quantity rests on the book.
        """
        # Store in orders dict
        self.orders[order.order_id] = order
        
        # Determine which side we're adding to
        if order.side == "B":
            # Add to buys dict at the appropriate price level
            if order.price not in self.buys:
                self.buys[order.price] = OrderedDict()

            self.buys[order.price][order.order_id] = order
        elif order.side == "S":  # order.side == 'S'
            # Add to sells dict at the appropriate price level
            if order.price not in self.sells:
                self.sells[order.price] = OrderedDict()

            self.sells[order.price][order.order_id] = order
        else:
            logger.error("Side attribute not recognised.")

    def amend_order(self, amend_obj):
        """Update sell object from both orders and buys/sells dictionaries."""
        if amend_obj.quantity == 0:
            self.cancel_order(amend_obj)
            return

        self.orders[amend_obj.order_id].quantity = amend_obj.quantity

    def cancel_order(self, cancel_obj):
        """Delete sell object from both orders and sells dictionaries."""
        order = self.orders[cancel_obj.order_id]
    
        if order.side == "B":
            del self.buys[order.price][order.order_id]

            # Delete the associated price key from the buys dict if empty
            if len(self.buys[order.price]) == 0:
                del self.buys[order.price]
        elif order.side == "S":
            del self.sells[order.price][order.order_id]

            # Delete the associated price key from the sells dict if empty
            if len(self.sells[order.price]) == 0:
                del self.sells[order.price]
        else:
            logger.error("Side attribute not recognised.")
        
        del self.orders[cancel_obj.order_id]