from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("",views.index,name='home'),
    path("contact",views.contact,name='contact'),
    path("napal",views.napal,name='napal'),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout",views.checkout,name='checkout'),
    path("tracker",views.tracker,name='tracker'),
    path("aboutus",views.aboutus,name='aboutus'),
    path("guide",views.guide,name='guide'),
    path("blockpost/<int:id>",views.blockpost,name='blockpost'),
    path("search",views.search,name='search'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
]
