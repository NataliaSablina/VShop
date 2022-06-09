from django.contrib import admin
from .models import Category, Product, ProductPhoto, Mark, DeliveryType, UserProductRelation

admin.site.register(Category)
admin.site.register(UserProductRelation)
admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(Mark)
admin.site.register(DeliveryType)

# Register your models here.
