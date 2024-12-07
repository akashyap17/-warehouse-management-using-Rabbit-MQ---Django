from django.core.management.base import BaseCommand
import pika
import json
from warehouse.models import Product, Category

class Command(BaseCommand):
    help = 'Start consuming messages from RabbitMQ'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='product_updates')

        def callback(ch, method, properties, body):
            data = json.loads(body)
            print(f"Received message: {data}")

            # Handle create action
            if data['action'] == 'create':
                product_data = data['product']
                category = Category.objects.get(id=product_data['category']['id'])
                Product.objects.create(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    stock_quantity=product_data['stock_quantity'],
                    category=category
                )
                print(f"Product created: {product_data['name']}")

            # Handle update action
            elif data['action'] == 'update':
                product_data = data['product']
                product = Product.objects.get(id=product_data['id'])
                product.name = product_data['name']
                product.description = product_data['description']
                product.price = product_data['price']
                product.stock_quantity = product_data['stock_quantity']
                product.save()
                print(f"Product updated: {product_data['name']}")

            # Handle delete action
            elif data['action'] == 'delete':
                product_data = data['product']
                product = Product.objects.get(id=product_data['id'])
                product.delete()
                print(f"Product deleted: {product_data['name']}")

        channel.basic_consume(queue='product_updates', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
