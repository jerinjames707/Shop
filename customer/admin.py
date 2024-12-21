from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from customer.models import CustomUser, Address

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if change and 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        obj.save()

admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)
