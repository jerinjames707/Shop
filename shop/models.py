from django.db import models
from customer.models import CustomUser, Address

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_average_rating(self):
        # Assuming there's a related `Review` model for calculating average rating
        reviews = self.reviews.all()
        total_rating = sum([review.rating for review in reviews])
        self.average_rating = total_rating / len(reviews) if reviews else 0
        self.save()

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating should be an integer, usually 1-5
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'



# Cart Model (no change required, but added for context)
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} in cart for {self.user.username}"

# Updated Order Model using Cart as a ForeignKey
class Order(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Foreign key to Cart
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')

    def __str__(self):
        return f"Order {self.id} - {self.cart.product.name} for {self.customer.username}"

    def save(self, *args, **kwargs):
        # Calculate the total price for the order based on the cart's product and quantity
        self.total_price = self.cart.product.price * self.cart.quantity

        # Reduce the product stock when an order is placed
        product = self.cart.product
        if product.quantity >= self.cart.quantity:
            product.quantity -= self.cart.quantity
            product.save()
        else:
            raise ValueError(f"Not enough stock for {product.name}. Available: {product.quantity}, Requested: {self.cart.quantity}")
        
        super().save(*args, **kwargs)  # Call the original save method to save the order



