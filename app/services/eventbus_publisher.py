from confluent_kafka import Producer
import json
import random

# Configuration for Kafka producer
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

# Initialize producer
producer = Producer(producer_config)

# Delivery report callback function
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Sample categories, including age-restricted ones
categories = ["alcohol", "tobacco", "snacks", "electronics"]

# Send messages with item details
def produce_messages():
    for i in range(10):
        # Creating a sample message with random categories
        item = {
            "name": f"item_{i}",
            "category": random.choice(categories),
            "price": round(random.uniform(1.0, 100.0), 2)
        }
        message = json.dumps(item)
        
        # Produce message
        producer.produce('test_topic', message, callback=delivery_report)
        producer.poll(0)  # Serve delivery callback queue

produce_messages()
producer.flush()
