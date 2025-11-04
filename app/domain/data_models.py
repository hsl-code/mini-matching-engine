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
    def __init__(self,
                 timestamp,
                 sequence_number,
                 symbol,
                 buy_order_id,
                 sell_order_id,
                 quantity,
                 price,
                 maker_order_id,
                 taker_side) -> None:
        self.timestamp = timestamp
        self.sequence_number = sequence_number
        self.symbol = symbol
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.quantity = quantity
        self.price = price
        self.maker_order_id = maker_order_id
        self.taker_side = taker_side

    def to_dict(self):
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