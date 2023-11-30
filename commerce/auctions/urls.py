from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.New_listing, name="new_listing"),
    path("listing/<str:pk>", views.listing_view, name="listing"),
    path("add/<str:pk>", views.add_watchlist, name="add_watchlist"),
    path("remove/<str:pk>", views.remove_watchlist, name="remove_watchlist"),
    path("close_bid/<str:pk>", views.close_bid, name='close_bid'),
    path("comment/<str:pk>", views.comment, name='comment'),
    path('watchlist', views.watchlist, name="watchlist"),
    path('categories', views.category,name='categories'),
    path('category/<str:category>', views.category_detail, name='category_detail')
]
