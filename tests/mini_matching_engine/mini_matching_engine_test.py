"""Test Cases

"""
from mini_matching_engine import MatchingEngine


def test_basic():
    """Test cases when the shortest feasible field period is not necessarily 1 day."""
    expected = [
        {
            "ts":1010,
            "seq":2,
            "symbol":"ABC",
            "buy_order_id":"B1",
            "sell_order_id":"S1",
            "qty":5,
            "price":100,
            "maker_order_id":"B1",
            "taker_side":"S"
         }
    ]

    engine = MatchingEngine(
        input_source="../fixtures/test_orders_basic.ndjson",
        datasource='file', 
        datastorage='dict_array'
        )
    output_stream = engine.process_stream()
    assert output_stream == expected

