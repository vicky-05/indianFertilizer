from django.urls import path
from authendicate import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('login', views.login_page,name='login'),
    # path('logout', views.logout_page,name='logout'),
    # path('user_profile', views.user_profile,name='user_profile'),
    # path('forgot', views.forgot_pass,name='forgot'),
    # path('reset_password', views.reset_password, name='reset_password'),
]