# Mini Matching Engine

## Overview

This is a single-pass matching engine that processes a stream of order events (create, amend, cancel) and outputs trades based on standard price-time priority rules. The engine is designed with scalability and extensibility in mind, allowing for future integration with real-time streaming systems like Kafka.

## Design Philosophy

While this implementation currently loads orders from NDJSON files, the architecture is designed to be **source-agnostic** and **sink-agnostic**. The core matching logic processes orders one-at-a-time using a while loop that pops from an input queue, making it naturally extensible to:

- **Data Sources**: File streams, Kafka consumers, WebSocket feeds, REST APIs
- **Data Sinks**: Files, databases (PostgreSQL, TimescaleDB), message queues, analytics pipelines

This design choice reflects how production matching engines work in real-time trading systems, where orders arrive as continuous streams rather than batches.

## Scope, Design Decisions, and Future Considerations

This implementation focuses primarily on correctness of the matching algorithm and clean, extensible architecture. The core objective is to ensure comprehensive test coverage of all matching scenarios while maintaining code that can scale into a production-grade real-time system. To that end, certain production features have been intentionally left for future work, including Kafka integration, metrics collection, and distributed systems coordination.

### Stream Processing and Kafka Integration

The while-loop processing pattern was chosen specifically to facilitate future streaming integration. The current implementation pops orders one-at-a-time from an in-memory queue, but this same pattern translates directly to consuming from a Kafka topic or WebSocket feed. We're treating the input as an unbounded stream rather than a batch, which reflects real trading environments where orders arrive continuously. During active trading hours, order flow can reach thousands of orders per second, making full in-memory storage of all historical data impractical.

Integrating with Kafka would be straightforward given the current architecture. The main processing loop would simply replace the in-memory queue pop with a Kafka consumer poll. Each message would be deserialized from the Kafka record value, processed through the same matching engine logic, and trades would be published to an output Kafka topic instead of written to a file. The abstraction layers for input and output queues are designed precisely for this kind of swap. Consumer group management, offset commits, and partition rebalancing would be handled by the Kafka client library, requiring minimal changes to the core matching logic.

One consideration for Kafka deployment is the partition strategy. Orders would need to be partitioned by symbol to ensure all orders for a given instrument are processed by the same consumer instance. This maintains the sequential processing guarantee necessary for correct order matching. Kafka's built-in partitioning based on message keys would handle this naturally, with the symbol field serving as the partition key.

### Distributed Systems Challenges

For distributed deployment, several challenges emerge that aren't addressed in this single-instance implementation. The matching engine is inherently stateful, maintaining the order book in memory, which complicates horizontal scaling. A partition-by-symbol strategy would be necessary, ensuring all orders for a given instrument route to the same consumer instance to avoid split-brain scenarios where multiple instances maintain conflicting views of the same order book.

Consensus issues arise when scaling horizontally. Consider a scenario where one consumer receives an order amendment while another receives a cancellation for the same order due to network partitioning or rebalancing. Which operation should win? Sequence numbers provide ordering guarantees at the message level, but distributed coordination requires additional mechanisms. Kafka's partition assignment ensures only one consumer processes a given partition at a time, which mitigates some of these concerns, but partition rebalancing during scaling events introduces temporary uncertainty.

The CAP theorem presents fundamental tradeoffs for distributed matching engines. In the event of network partitions, the system must choose between availability (continuing to accept and process orders) and consistency (ensuring all nodes agree on order book state). Trading systems typically sacrifice some availability to maintain consistency, as incorrect order matching has regulatory and financial implications. This might mean rejecting orders during partition events rather than risking dual execution or incorrect matching.

State management becomes critical in distributed scenarios. While this implementation keeps everything in memory, a production system would need mechanisms for state recovery after failures. Options include periodic snapshots to durable storage, replaying Kafka topics from known offsets, or using distributed state stores like RocksDB. The choice depends on acceptable recovery time objectives and data durability requirements.

### Network Reliability and Idempotency

Network reliability is another production concern not addressed in this implementation. Real-world issues like AWS EBS storms or DNS failures can cause duplicate messages, out-of-order delivery, or message loss. AWS has experienced incidents where network retries led to messages being delivered multiple times or stored events being replayed unexpectedly. Proper handling would require idempotency keys using sequence numbers, deduplication windows, and careful consideration of at-least-once versus exactly-once delivery semantics.

The current implementation assumes perfect message delivery and ordering. In production, each message would need to include monotonically increasing sequence numbers that the engine validates. Messages arriving out of sequence would trigger alerts and potentially be rejected or queued for reordering. Duplicate sequence numbers would be detected and ignored to prevent double-execution of trades. This validation layer would sit before the matching engine, filtering problematic messages before they corrupt the order book state.

Kafka provides some built-in guarantees here. With proper configuration, Kafka can provide exactly-once semantics within a Kafka-to-Kafka pipeline, meaning a message is consumed exactly once and any output messages are produced exactly once. However, this doesn't extend to external systems, so additional idempotency mechanisms would still be necessary when writing to databases or calling external APIs.

### Metrics and Observability

Metrics collection and observability are completely absent from the current implementation but would be essential for production deployment. Key metrics to track would include order processing latency (time from order receipt to trade execution), throughput (orders processed per second), order book depth at various price levels, and trade volume. These metrics would typically be exported to a monitoring system like Prometheus or StatsD for real-time dashboards and alerting.

Latency measurements would need to be instrumented at multiple points: message receipt from Kafka, deserialization time, matching engine processing time, and trade publication time. Percentile distributions (p50, p95, p99) would be more informative than simple averages, as they reveal tail latencies that affect user experience. High p99 latencies might indicate garbage collection pauses, network issues, or inefficient matching logic that needs optimization.

Distributed tracing would provide visibility into request flows across multiple services. In a microservices architecture, a single order might flow through multiple components: ingestion service, validation service, matching engine, trade publication, and settlement. Tracing tools like Jaeger or Zipkin would allow debugging of latency issues by showing exactly where time is spent in the processing pipeline.

Structured logging is another critical observability component not implemented here. The current basic logging would need to be enhanced with structured formats (JSON) including request IDs, timestamps, and contextual metadata. Logs would be aggregated in a centralized system like Elasticsearch or Splunk, allowing correlation of events across multiple instances and rapid investigation when issues occur.

Alerting thresholds would be defined based on these metrics. For example, if order processing latency exceeds 100ms at p99, or if the error rate exceeds 0.1%, alerts would notify on-call engineers. Dead letter queues would capture messages that fail processing repeatedly, allowing manual investigation without blocking the main processing pipeline.

### Data Validation

Data validation is minimal in the current implementation, with only basic checks and logging for anomalies. Production systems would validate sequence number monotonicity, timestamp ordering, price and quantity sanity checks, and symbol existence. These validations would likely be extracted into a separate validation layer before orders reach the matching engine. Invalid messages would be routed to a dead letter queue for investigation rather than causing processing failures or corrupting the order book state.

### Output Integration

Output flexibility was a key design consideration. While the current implementation writes to NDJSON files, the architecture supports multiple sink types. For dashboarding with tools like Grafana, trades could be written to PostgreSQL with TimescaleDB extensions for efficient time-series queries, though this adds 10-50ms of latency per write. For sub-second requirements, direct streaming to in-memory data grids like Redis or WebSocket feeds would be more appropriate. The abstraction of an output queue makes swapping between these implementations straightforward.

In a Kafka-based architecture, trades would be published to a separate Kafka topic, allowing multiple downstream consumers to process trade data independently. One consumer might write to a database for historical analysis, another might update a real-time dashboard, and a third might trigger settlement processes. This fan-out pattern provides flexibility and decouples the matching engine from specific downstream requirements.

### Current Limitations

The implementation is entirely in-memory with no persistence layer, optimized for speed and simplicity during development. It's also single-threaded without any concurrency controls, which is acceptable for this scope but would need addressing for production deployment. There's no partition tolerance, no graceful degradation during failures, and no circuit breakers or backpressure mechanisms. These are intentional scope decisions to focus on correctness and clean architecture.

The system currently has no awareness of time-based market events like market open/close or trading halts, which real matching engines must handle. There's also no support for different order types beyond basic limit orders, no support for multiple instruments being processed in parallel, and no configuration management for tuning processing parameters.

## Test Cases

### Basic Scenarios
- ✅ Simple buy-sell match
- ✅ Partial fills with resting orders
- ✅ Multiple trades from single order
- ✅ No match (order rests on book)

### Order Lifecycle
- ✅ Create → Match → Trade
- ✅ Create → Amend → Match
- ✅ Create → Cancel (before match)
- ✅ Amend with qty=0 (treat as cancel)

### Edge Cases
- ✅ Duplicate order_id (should ignore)
- ✅ Cancel non-existent order (log warning)
- ✅ Amend non-existent order (log warning)
- ✅ Out-of-sequence numbers (validation)
- ✅ Multiple orders at same price (FIFO)

### Price Priority
- ✅ Best price executes first (not FIFO across prices)
- ✅ Crossing orders match immediately
- ✅ Non-crossing orders rest on book

## Setup & Usage

### Running the Engine
```
python3 app/server.py
```

### Running Tests
```
python3 -m pytest tests/
```
