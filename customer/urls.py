from django.urls import path
from customer.views import RegisterView, CustomAuthToken, LogoutView, AddressListCreateView, AddressRetrieveUpdateDestroyView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='customer-signup'),
    path('login/', CustomAuthToken.as_view(), name='customer-login'),
    path('logout/', LogoutView.as_view(), name='customer-logout'),
    path('address/', AddressListCreateView.as_view(), name='address-create'),
    path('address/<int:pk>/', AddressRetrieveUpdateDestroyView.as_view(), name='address-update'),
]