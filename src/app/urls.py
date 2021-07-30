from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home_Page, name='Home_Page'),
    path('app',views.App_Page, name='App_Page'),
    path('login',views.Login_Page, name='Login_Page'),
    path('register',views.Register_Page, name='Register_Page'),
    # path('upload_id',views.upload_id, name='upload_id'),
]
