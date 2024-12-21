from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import Product, Order, Cart, Review
from shop.serializers import ProductSerializer, OrderSerializer, CartSerializer, ReviewSerializer
from customer.models import Address
from rest_framework import status


# Product List View (only accessible by logged-in users)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# Admin Product Management Views
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser]


# Order Status Update View (Admin only)
class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        order = self.get_object()
        order.status = serializer.validated_data['status']
        order.save()


# Cart Management View (Only logged-in users can add/remove products)
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Review Management View (only logged-in users can create a review)
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the review is linked to the current user and product
        serializer.save(user=self.request.user)


# Order Creation View (Allows users to create orders)
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # The order creation logic is handled in the serializer, so no need to override here
        return super().perform_create(serializer)
