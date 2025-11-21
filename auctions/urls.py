from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("place_bid/<int:listing_id>/", views.place_bid, name="place_bid"),
    path("category", views.category, name="category"),
    path('category_items/<int:category_id>/', views.category_items, name='category_items'),
    path("watchlist", views.watchlist, name='watchlist'),
    path("add_watchlist/<int:listing_id>/", views.add_watchlist, name='add_watchlist'),
    path("close_auction/<int:listing_id>/", views.close_auction, name='close_auction'),
    path("my_listings", views.my_listings, name="my_listings"),
    path("won_auctions", views.won_auctions, name='won_auctions')
   
]
