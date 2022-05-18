from django.contrib import admin
from .models import Country, City, Currency

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Currency)

# Register your models here.
