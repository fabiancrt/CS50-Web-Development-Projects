from django.urls import path

from . import views

#these are the necessary urls for the project , nothing special here

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_product", views.add_product_view, name="add_product"),
    path("product/<int:product_id>", views.product_detail_view, name="product_detail"),
    path('categories/', views.categories_view, name='categories'),
    path('categories/<str:category_name>/', views.category_products_view, name='category_products'),
    path('place_bid/<int:product_id>/', views.place_bid, name='place_bid'),
    path('product/<int:product_id>/close/', views.close_auction, name='close_auction'),
    path("participated_auctions", views.participated_auctions_view, name="participated_auctions"),  # New URL pattern
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/add/<int:product_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:product_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('my_auctions', views.my_auctions, name='my_auctions'),
    path('delete_comment/<int:review_id>/', views.delete_comment, name='delete_comment'),
]   
