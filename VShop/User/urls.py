from django.urls import path
from .views import main_page, index2


urlpatterns = [
    path('', main_page, name='main_page'),
    path('index', index2, name='index2')
]