from django.urls import path
from . import views
from .views import ProductView

urlpatterns = [
    path('product_page/<int:pk>', ProductView.as_view(), name="product_page"),
]