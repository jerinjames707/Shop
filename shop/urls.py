from django.urls import path
from shop import views

urlpatterns = [
    # Product Views
    path('products/', views.ProductListView.as_view(), name='product-list'),  # Product list
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),  # Admin can create products
    path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),  # Admin can update product
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),  # Admin can delete product

    # Order Views
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),  # Create order
    path('orders/status-update/<int:pk>/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),  # Admin can update order status

    # Cart Views
    path('cart/', views.CartView.as_view(), name='cart-list-create'),  # View and create cart items

    # Review Views
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),  # Create review
]
