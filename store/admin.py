from django.contrib import admin
from .models import Perfume, ShoppingCart, User, Recommendations, CartItem

@admin.register(Perfume, ShoppingCart, User, Recommendations, CartItem)
class PersonAdmin(admin.ModelAdmin):
    pass
