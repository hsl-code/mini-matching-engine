"""Data models for all order objects.

todo make an order interface?
"""

class Buy:
    def __init__(self, buy_dict) -> None:
        self.type = buy_dict["type"]
        self.timestamp = buy_dict["ts"]
        self.sequence_number = buy_dict["seq"]
        self.symbol = buy_dict["symbol"]
        self.side = buy_dict["side"]
        self.order_id = buy_dict["order_id"]
        self.price = buy_dict["price"]
        self.quantity = buy_dict["qty"]


class Sell:
    def __init__(self, sell_dict) -> None:
        self.type = sell_dict["type"]
        self.timestamp = sell_dict["ts"]
        self.sequence_number = sell_dict["seq"]
        self.symbol = sell_dict["symbol"]
        self.side = sell_dict["side"]
        self.order_id = sell_dict["order_id"]
        self.price = sell_dict["price"]
        self.quantity = sell_dict["qty"]


class Amend:
    def __init__(self, amend_dict) -> None:
        self.type = amend_dict["type"]
        self.timestamp = amend_dict["ts"]
        self.sequence_number = amend_dict["seq"]
        self.symbol = amend_dict["symbol"]
        self.order_id = amend_dict["order_id"]
        self.quantity = amend_dict["qty"]


class Cancel:
    def __init__(self, cancel_dict) -> None:
        self.type = cancel_dict["type"]
        self.timestamp = cancel_dict["ts"]
        self.sequence_number = cancel_dict["seq"]
        self.symbol = cancel_dict["symbol"]
        self.order_id = cancel_dict["order_id"]


class Trade:
    def __init__(self) -> None:
        self.timestamp = None
        self.sequence_number = None
        self.symbol = None
        self.buy_order_id = None
        self.sell_order_id = None
        self.quantity = None
        self.price = None
        self.maker_order_id = None
        self.taker_side = None

    def to_json(self):
        return {
            "ts":self.timestamp,
            "seq":self.sequence_number,
            "symbol":self.symbol,
            "buy_order_id":self.buy_order_id,
            "sell_order_id":self.sell_order_id,
            "qty":self.quantity,
            "price":self.price,
            "maker_order_id":self.maker_order_id,
            "taker_side":self.taker_side,
            }