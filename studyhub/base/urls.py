from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('', views.home, name='home'),
    path('lobby/<str:pk>', views.lobby, name='lobby'),

    path('create_lobby/', views.create_lobby, name='create_lobby'),
    path('update_lobby/<str:pk>', views.update_lobby, name='update_lobby'),
    path('delete_lobby/<str:pk>', views.delete_lobby, name='delete_lobby'),
]
