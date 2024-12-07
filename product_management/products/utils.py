# products/utils.py
import pika
import json


def send_message_to_queue(data):
    """Send message to RabbitMQ queue."""
    # Establish connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (this ensures that the queue exists)
    channel.queue_declare(queue='product_updates', durable=False)  # 'durable' ensures persistence

    # Convert data (typically a dictionary) to JSON
    message = json.dumps(data)

    # Publish the message to the queue
    channel.basic_publish(
        exchange='',  # Default exchange
        routing_key='product_updates',  # Queue name
        body=message,  # Message content
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent (optional, recommended for durability)
        )
    )

    print(" [x] Sent message to product_updates queue")

    # Close the connection
    connection.close()
