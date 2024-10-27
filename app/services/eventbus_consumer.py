from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from age_verification_plugin import requires_age_verification



# Configuration for Kafka consumer
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

# Initialize consumer
consumer = Consumer(consumer_config)
consumer.subscribe(['test_topic'])



# Consume messages
print("Listening for messages...")
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        # Check if there's a message
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
        else:
            # Decode the message and process it
            message_value = msg.value().decode('utf-8')
            print(f"Received: {message_value}")
            
            # Deserialize JSON message
            try:
                item = json.loads(message_value)  # assuming JSON format for messages
                
                # Check if item requires age verification
                if requires_age_verification(item):
                    print(f"Age verification required for item: {item['name']}, Category: {item['category']}")
                else:
                    print(f"No age verification needed for item: {item['name']}, Category: {item['category']}")
            except json.JSONDecodeError:
                print("Received non-JSON message:", message_value)

finally:
    # Ensure the consumer is closed on exit
    consumer.close()
