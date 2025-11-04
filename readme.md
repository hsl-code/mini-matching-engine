# Challenge: Mini Matching Engine (Python)

Goal: Build a single‑pass matching engine that consumes a stream of newline‑delimited JSON (NDJSON) order events and emits a stream of trades (also NDJSON).

We'll go over your solution in the follow up interview as well working through some additional changes.

Check the `example` folder for sample input and output files.

## Input events

### `create`

Matching rule: Standard price–time priority.

Buy crosses if best_ask_price <= incoming_buy_price.

Sell crosses if best_bid_price >= incoming_sell_price.

Trade price = resting (maker) order’s price.

Partial fills produce multiple trades; any remainder rests on the book. So if a buy is created for qty=10 and matches against two sells for qty=4 and qty=3, that produces two trades (qty=4 and qty=3) and leaves a resting buy order for qty=3.

Repeated create with the same order_id while active → ignore.

#### Example

```json
{"type":"create","ts":1000000,"seq":1,"symbol":"ABC","side":"S","order_id":"S1","price":101,"qty":4}
{"type":"create","ts":1000002,"seq":2,"symbol":"ABC","side":"B","order_id":"B1","price":102,"qty":5}
```

Will produce one trade:

```json
{
  "ts": 1000002,
  "seq": 2,
  "symbol": "ABC",
  "buy_order_id": "B1",
  "sell_order_id": "S1",
  "qty": 4,
  "price": 101,
  "maker_order_id": "S1",
  "taker_side": "B"
}
```

As well as leaving a resting buy order for qty=1 at price=102.

### `amend`

Change a quantity of an existing order based on a order_id.

If qty=0, treat as cancel.

#### Example

```json
{
  "type": "amend",
  "ts": 1000005,
  "seq": 3,
  "symbol": "ABC",
  "order_id": "B1",
  "qty": 2
}
```

### `cancel`

Cancel removes the order if present; unknown cancels are ignored. Doesn't produce trades.

#### Example

```json
{
  "type": "cancel",
  "ts": 1000007,
  "seq": 4,
  "symbol": "ABC",
  "order_id": "S1"
}
```

## Output

Each trade event should include:

- ts
- seq (from the incoming order that triggered the trade)
- symbol
- buy_order_id
- sell_order_id
- qty
- price
- maker_order_id
- taker_side
