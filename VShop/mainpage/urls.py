from django.urls import path

from mainpage.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('<str:name>', HomePageView.as_view(), name='home_page'),
]