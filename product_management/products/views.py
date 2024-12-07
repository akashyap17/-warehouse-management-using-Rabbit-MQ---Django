# from django.shortcuts import render
#
# from rest_framework import viewsets
# from .models import Category, Product
# from .serializers import CategorySerializer, ProductSerializer
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.select_related('category').all()
#     serializer_class = ProductSerializer
#


# products/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Category
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .utils import send_message_to_queue  # Import the publisher function

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # Create the product first
        product = serializer.save()

        # Prepare the product data to send in the message
        product_data = ProductSerializer(product).data
        message_data = {
            'action': 'create',  # Action type (create/update/delete)
            'product': product_data  # Send the serialized product data
        }

        # Call the publisher function to send the message to RabbitMQ
        print(f"Sending message to RabbitMQ: {message_data}")  # Debugging line
        send_message_to_queue(message_data)

    def perform_update(self, serializer):
        # Update the product first
        product = serializer.save()

        # Prepare the product data to send in the message
        product_data = ProductSerializer(product).data
        message_data = {
            'action': 'update',  # Action type (create/update/delete)
            'product': product_data  # Send the serialized product data
        }

        # Call the publisher function to send the message to RabbitMQ
        send_message_to_queue(message_data)

    def perform_destroy(self, instance):
        # Serialize the product data before deleting
        product_data = ProductSerializer(instance).data
        message_data = {
            'action': 'delete',  # Action type (create/update/delete)
            'product': product_data  # Send the serialized product data
        }

        # Call the publisher function to send the message to RabbitMQ
        send_message_to_queue(message_data)

        # Proceed with the deletion
        instance.delete()



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        # Create the category first
        category = serializer.save()

        # Prepare the category data to send in the message
        category_data = CategorySerializer(category).data
        message_data = {
            'action': 'create',  # Action type (create/update/delete)
            'category': category_data  # Send the serialized category data
        }

        # Call the publisher function to send the message to RabbitMQ
        send_message_to_queue(message_data)

    def perform_update(self, serializer):
        # Update the category first
        category = serializer.save()

        # Prepare the category data to send in the message
        category_data = CategorySerializer(category).data
        message_data = {
            'action': 'update',  # Action type (create/update/delete)
            'category': category_data  # Send the serialized category data
        }

        # Call the publisher function to send the message to RabbitMQ
        send_message_to_queue(message_data)

    def perform_destroy(self, instance):
        # Serialize the category data before deleting
        category_data = CategorySerializer(instance).data
        message_data = {
            'action': 'delete',  # Action type (create/update/delete)
            'category': category_data  # Send the serialized category data
        }

        # Call the publisher function to send the message to RabbitMQ
        send_message_to_queue(message_data)

        # Proceed with the deletion
        instance.delete()
