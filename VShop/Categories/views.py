from django.shortcuts import render, redirect
from django.views import View
from country.models import Country, City
from Categories.models import Product


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'product_page.html', {'product': product})

