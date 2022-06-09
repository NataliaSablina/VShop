from django.urls import path

from mainpage.views import HomePageView, SearchProductsView, SearchNotDoneView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('search_done', SearchProductsView.as_view(), name='search_done'),
    path('search_not_done', SearchNotDoneView.as_view(), name='search_not_done'),
    path('<str:name>', HomePageView.as_view(), name='home_page'),
]