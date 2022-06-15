from django.urls import path
from . import views
from .views import ProductView, SearchResultsView, CategoriesProductsView, CategoryProductsView, like_product, \
    RecommendedProductsView, CommentLikeView, CommentsView, CreateBookMarkView, UserBookmarksListView, \
    SortFilterPageView, SortProducts

urlpatterns = [
    path('product_page/<int:pk>', ProductView.as_view(), name="product_page"),
    path('search', SearchResultsView.as_view(), name='search_results'),
    path('like/<int:product_id>/<str:back_url>', like_product, name='like'),
    path('bookmarks/<int:product_id>/<str:back_url>', CreateBookMarkView.as_view(), name='bookmarks'),
    path('categories_product_listing', CategoriesProductsView.as_view(), name='categories_product_listing'),
    path('category_product_listing/<int:pk>', CategoryProductsView.as_view(), name='category_product_listing'),
    path('none', RecommendedProductsView.as_view(), name='none'),
    path('sort/<str:back_url>', SortProducts.as_view(), name='sort'),
    path('sort_filter_page/<int:sorting_id>', SortFilterPageView.as_view(), name='sort_filter_page'),
    path('sort_filter_page/<int:sorting_id>/<str:minmax>', SortFilterPageView.as_view(), name='sort_filter_page'),
    path('sort_filter_page/<int:sorting_id>/<str:filter_str>/<str:minmax>', SortFilterPageView.as_view(),
         name='sort_filter_page'),
    path('comments/<int:pk>', CommentsView.as_view(), name='comments'),
    path('user_bookmarks', UserBookmarksListView.as_view(), name='user_bookmarks'),
    # path('comment_product/<int:pk>', comment_view, name='comment_product'),
    # path('comment_comment/<int:pk>/<int:comment_id>', comment_comment_view, name='comment_comment'),
    path('comment_like/<int:pk>/<int:product_id>/<str:back_url>', CommentLikeView.as_view(), name='comment_like'),
]
