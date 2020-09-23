from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('register', views.registerPage, name="registerPage"),
    path('login', views.loginPage, name="loginPage"),

    path('', views.home, name="home"),
    path('products', views.products, name='products'),
    path('customers/<str:pk_test>', views.customers, name="customer"),
    path('createOrder/<str:pk>', views.createOrder, name="createOrder"),
    path('updateOrder/<str:pk>', views.updateOrder, name="updateOrder"),
    path('deleteOrder/<str:pk>', views.deleteOrder, name="deleteOrder"),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('userPage', views.userPage, name="userPage"),
    path('account/', views.accountSettings, name="account")

]
