from django.urls import path
from promocode.views import AvailablePromosView, PromoListView, PromoPageView, AllAvailablePromosCategoriesView

urlpatterns = [
    path('available_promos', AvailablePromosView.as_view(), name='available_promos'),
    path('promos_category_page/<int:pk>', PromoListView.as_view(), name="promos_category_page"),
    path('promo_page/<int:pk_1>/<int:pk_2>', PromoPageView.as_view(), name="promo_page"),
    path('all_promo_categories', AllAvailablePromosCategoriesView.as_view(), name="all_promo_categories"),

]
