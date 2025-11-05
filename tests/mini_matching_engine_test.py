from mini_matching_engine import MatchingEngine


def test_basic():
    """Test simple buy-sell sequence."""
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
        input_source="tests/fixtures/test_orders_basic.ndjson",
        datasource='file', 
        datastorage='dict_array'
        )
    output_stream = engine.process_stream()
    assert output_stream == expected


def test_basic_2():
    expected = [
        {
            "ts":1000,
            "seq":2,
            "symbol":"ABC",
            "buy_order_id":"B1",
            "sell_order_id":"S1",
            "qty":5,"price":50,
            "maker_order_id":"S1",
            "taker_side":"B"
        }
    ]

    engine = MatchingEngine(
        input_source="tests/fixtures/test_orders_basic_2.ndjson",
        datasource='file', 
        datastorage='dict_array'
        )
    output_stream = engine.process_stream()
    assert output_stream == expected


def test_one_sell_two_buys_with_surplus():
    """Test case where there are 2 buys for a sell but there is surplus quantity remaining to be sold."""
    expected = [
        {"ts":1000,"seq":2,"symbol":"ABC","buy_order_id":"B1","sell_order_id":"S1","qty":10,"price":50,"maker_order_id":"S1","taker_side":"B"},
        {"ts":1001,"seq":3,"symbol":"ABC","buy_order_id":"B2","sell_order_id":"S1","qty":20,"price":50,"maker_order_id":"S1","taker_side":"B"}
    ]

    engine = MatchingEngine(
        input_source="tests/fixtures/test_orders_basic_3.ndjson",
        datasource='file', 
        datastorage='dict_array'
        )
    output_stream = engine.process_stream()
    assert output_stream == expected