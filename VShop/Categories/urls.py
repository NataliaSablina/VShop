from django.urls import path
from . import views
from .views import ProductView, SearchResultsView, CategoriesProductsView, CategoryProductsView

urlpatterns = [
    path('product_page/<int:pk>', ProductView.as_view(), name="product_page"),
    path('search', SearchResultsView.as_view(), name='search_results'),
    path('categories_product_listing', CategoriesProductsView.as_view(), name='categories_product_listing'),
    path('category_product_listing/<int:pk>', CategoryProductsView.as_view(), name='category_product_listing'),
]
