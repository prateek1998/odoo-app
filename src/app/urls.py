from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home_view, name='home'),
    path('',views.app_view, name='app'),
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('register',views.register_view, name='register'),
    path('edit_manual',views.edit_manual, name='edit_manual'),
    # path('upload_id',views.upload_id, name='upload_id'),
]
