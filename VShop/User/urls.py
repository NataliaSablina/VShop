from django.urls import path
from .views import index2, HomePage, UserPage, logout_view


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('index', index2, name='index2'),
    path('user_page/<str:email>', UserPage.as_view(), name="user_page"),
    path('logout', logout_view, name='logout'),

]