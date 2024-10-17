
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('login_view', views.login_view, name='login_view'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('upload_images',views.upload_images,name='upload_images'),
]
