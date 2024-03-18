from django.contrib import admin
from .models import Perfume, ShoppingCart, User, Recommendations

@admin.register(Perfume, ShoppingCart, User, Recommendations)
class PersonAdmin(admin.ModelAdmin):
    pass
