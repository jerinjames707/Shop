from rest_framework import serializers
from shop.models import Product, Order, Cart, Review
from customer.models import Address

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'average_rating', 'reviews']

# cart Serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

    def validate_quantity(self, value):
        """
        Validates that the quantity is positive and doesn't exceed the available stock of the product.
        """
        product = self.instance.product if self.instance else self.initial_data['product']
        
        # Check if the quantity is positive
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

        # Check if the quantity doesn't exceed the available stock
        if value > product.quantity:
            raise serializers.ValidationError(
                f"Not enough stock available. Only {product.quantity} items are in stock."
            )

        return value

    def validate(self, data):
        """
        Validates the cart item for existing entries and any other conflicts.
        """
        # Check if the product is already in the cart for the same user
        if Cart.objects.filter(user=data['user'], product=data['product']).exists():
            raise serializers.ValidationError(
                "This product is already in your cart. Please update the quantity if needed."
            )
        
        return data

    def create(self, validated_data):
        """
        Handles the creation of a new cart item, ensuring stock is updated accordingly.
        """
        try:
            # Ensure that we update the stock of the product
            product = validated_data['product']
            quantity = validated_data['quantity']
            
            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock available. Only {product.quantity} items are in stock."
                )

            # Deduct the quantity from the product stock
            product.quantity -= quantity
            product.save()

            # Create the cart item
            cart_item = Cart.objects.create(**validated_data)
            return cart_item
        
        except Exception as e:
            raise serializers.ValidationError(f"Error occurred while creating cart item: {str(e)}")

    def update(self, instance, validated_data):
        """
        Handles the update of an existing cart item, ensuring stock is updated accordingly.
        """
        try:
            # Check if the quantity is valid and doesn't exceed stock
            product = validated_data['product']
            new_quantity = validated_data['quantity']
            
            if new_quantity > product.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock available. Only {product.quantity} items are in stock."
                )
            
            # Update the stock of the product
            product.quantity -= new_quantity
            product.save()

            # Update the cart item
            instance.quantity = new_quantity
            instance.save()

            return instance

        except Exception as e:
            raise serializers.ValidationError(f"Error occurred while updating cart item: {str(e)}")
        

class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    shipping_address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['product_id', 'quantity', 'shipping_address_id', 'status', 'total_price']

    def create(self, validated_data):
        product = validated_data['product_id']
        user = self.context['request'].user
        address = validated_data.get('shipping_address_id', None)

        # Get the user's cart items
        cart_items = Cart.objects.filter(user=user)

        orders = []
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            total_price_for_item = product.price * quantity

            # Check if enough stock is available
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock available for {product.name}. Only {product.quantity} items are in stock.")

            # Update product stock
            product.quantity -= quantity
            product.save()

            # If no address is provided, create a new one
            if not address:
                address_data = self.context['request'].data.get('address', None)
                if not address_data:
                    raise serializers.ValidationError("Address data is required when no address is provided.")
                
                address = Address.objects.create(
                    user=user,
                    **address_data  # Assuming address data contains the necessary fields for Address model
                )

            # Create the order
            order = Order.objects.create(
                customer=user,
                product=cart_item.product,
                quantity=quantity,
                total_price=total_price_for_item,
                shipping_address=address,
            )
            orders.append(order)

        return orders  # Return the list of orders


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username of the user who made the review

    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment']
