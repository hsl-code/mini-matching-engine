from logger import getLogger
logger = getLogger(__name__)


from collections import OrderedDict
from sortedcontainers import SortedDict
from domain.data_models import Trade



class OrderBook:
    def __init__(self) -> None:
        """Order Book class

        buys - SortedDict with buys with price as keys(sorted), and OrderedDicts with order_id as nested keys
        self.buys = {price: OrderedDict({order_id: order_obj})}

        sells - SortedDict with sells with price as keys(sorted), and OrderedDicts with order_id as nested keys
        self.buys = {price: OrderedDict({order_id: order_obj})}

        orders - dict with all orders with order_id as keys
        trades - dict containing output trades
        """
        self.buys = SortedDict()
        self.sells = SortedDict()
        self.orders = SortedDict()
        self.trades = []

    def add_order(self, order):
        """Add an order to the book and attempt to match it.
    
        If the order crosses with existing orders, execute trades.
        Any remaining quantity rests on the book.
        """
        # Store in orders dict
        self.orders[order.order_id] = order
        
        if order.side == "B":
            self._match_buy_order(order)
        elif order.side == "S":
            self._match_sell_order(order)
        else:
            logger.error("Side attribute not recognised.")
            return
        
        # If order has remaining quantity, add it to the book
        if order.quantity > 0:
            self._add_order_to_book(order)
    
    def _add_order_to_book(self, order):
        """Add order to the book (after matching attempts)."""
        # Store in orders dict
        self.orders[order.order_id] = order
        
        # Add to appropriate side
        if order.side == "B":
            if order.price not in self.buys:
                self.buys[order.price] = OrderedDict()
            self.buys[order.price][order.order_id] = order
        elif order.side == "S":
            if order.price not in self.sells:
                self.sells[order.price] = OrderedDict()
            self.sells[order.price][order.order_id] = order
    
    def _match_buy_order(self, buy_order):
        """Match an incoming buy order against resting sell orders."""
        while self.sells and buy_order.quantity > 0:
            # Get best ask (lowest sell price)
            best_ask = self.sells.keys()[0]
            logger.info("Best ask obtained: {}".format(best_ask))
            
            # Check if buy crosses with best ask
            if buy_order.price < best_ask:
                logger.info("No match possible, exiting...")
                break  # No match possible
            
            # Get the FIRST (earliest) sell order at this price
            logger.info("Getting earliest sell order at best ask price...")
            sell_orders_at_price = self.sells[best_ask]
            first_sell_id = next(iter(sell_orders_at_price))
            sell_order = sell_orders_at_price[first_sell_id]
            
            # Determine trade quantity
            logger.info("Determining trade quantity...")
            trade_qty = min(buy_order.quantity, sell_order.quantity)
            
            # Create trade (maker = sell order, taker = buy order)
            logger.info("New trade made with quantity {}".format(trade_qty))
            trade = Trade(
                timestamp=buy_order.timestamp,
                sequence_number=buy_order.sequence_number,
                symbol=buy_order.symbol,
                buy_order_id=buy_order.order_id,
                sell_order_id=sell_order.order_id,
                quantity=trade_qty,
                price=best_ask,  # Trade at maker's price
                maker_order_id=sell_order.order_id,
                taker_side="B"
            )
            logger.info("New trade added to output stream.")
            self.trades.append(trade)
            print(self.trades)
            
            # Update quantities
            logger.info("Updating trade quantities.")
            buy_order.quantity -= trade_qty
            sell_order.quantity -= trade_qty
            
            # Remove sell order if fully filled
            logger.info("Cleaning up orders post-trade...")
            if sell_order.quantity == 0:
                del sell_orders_at_price[first_sell_id]
                del self.orders[first_sell_id]
                
                # Clean up empty price level
                if len(sell_orders_at_price) == 0:
                    del self.sells[best_ask]

    def _match_sell_order(self, sell_order):
        """Match an incoming sell order against resting buy orders."""
        while self.buys and sell_order.quantity > 0:
            # Get best bid (highest buy price)
            best_bid = self.buys.keys()[-1]
            
            # Check if sell crosses with best bid
            if sell_order.price > best_bid:
                logger.info("No match possible, exiting...")
                break  # No match possible
            
            # Get the FIRST (earliest) buy order at this price
            logger.info("Getting earliest buy order at best bid price...")
            buy_orders_at_price = self.buys[best_bid]
            first_buy_id = next(iter(buy_orders_at_price))
            buy_order = buy_orders_at_price[first_buy_id]
            
            # Determine trade quantity
            logger.info("Determining trade quantity...")
            trade_qty = min(buy_order.quantity, sell_order.quantity)
            
            # Create trade (maker = buy order, taker = sell order)
            logger.info("New trade made with quantity {}".format(trade_qty))
            trade = Trade(
                timestamp=sell_order.timestamp,
                sequence_number=sell_order.sequence_number,
                symbol=sell_order.symbol,
                buy_order_id=buy_order.order_id,
                sell_order_id=sell_order.order_id,
                quantity=trade_qty,
                price=best_bid,  # Trade at maker's price
                maker_order_id=buy_order.order_id,
                taker_side="S"
            )
            logger.info("New trade added to output stream.")
            self.trades.append(trade)
            print(self.trades)
            
            # Update quantities
            logger.info("Updating trade quantities.")
            buy_order.quantity -= trade_qty
            sell_order.quantity -= trade_qty
            
            # Remove buy order if fully filled
            logger.info("Cleaning up orders post-trade...")
            if buy_order.quantity == 0:
                del buy_orders_at_price[first_buy_id]
                del self.orders[first_buy_id]
                
                # Clean up empty price level
                if len(buy_orders_at_price) == 0:
                    del self.buys[best_bid]

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
    
    def get_trades(self):
        """Return all trades as list of trade objects."""
        return self.trades