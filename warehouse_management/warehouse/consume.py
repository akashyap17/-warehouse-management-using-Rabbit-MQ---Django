# warehouse/consume_messages.py
import pika
import json
from warehouse.models import Product, Category

def consume_messages():
    # Establish a connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (this ensures that the queue exists)
    channel.queue_declare(queue='product_updates')

    def callback(ch, method, properties, body):
        """Callback to handle incoming messages."""
        data = json.loads(body)
        print(f"Received message: {data}")

        # Process the message based on action type
        if data['action'] == 'create':
            # Handle product creation in App 2
            product_data = data['product']
            category = Category.objects.get(id=product_data['category']['id'])  # Assuming category data is included
            Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock_quantity=product_data['stock_quantity'],
                category=category
            )
            print(f"Product created: {product_data['name']}")

        elif data['action'] == 'update':
            # Handle product update in App 2
            product_data = data['product']
            product = Product.objects.get(id=product_data['id'])
            product.name = product_data['name']
            product.description = product_data['description']
            product.price = product_data['price']
            product.stock_quantity = product_data['stock_quantity']
            product.save()
            print(f"Product updated: {product_data['name']}")

        elif data['action'] == 'delete':
            # Handle product deletion in App 2
            product_data = data['product']
            product = Product.objects.get(id=product_data['id'])
            product.delete()
            print(f"Product deleted: {product_data['name']}")

    # Start consuming messages from RabbitMQ
    channel.basic_consume(queue='product_updates', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
