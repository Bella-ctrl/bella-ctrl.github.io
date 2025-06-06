from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('watchlist/<int:listing_id>/', views.watchlist_toggle, name='watchlist_toggle'),
    path('bid/<int:listing_id>/', views.place_bid, name='place_bid'),
    path('close/<int:listing_id>/', views.close_auction, name='close_auction'),
    path('comment/<int:listing_id>/', views.add_comment, name='add_comment'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:category_code>/', views.category_listings, name='category_listings'),
]
