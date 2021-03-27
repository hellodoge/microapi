from django.urls import path
from django.contrib.auth.views import LoginView
from .views import signup_view, logout_view


urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup')
]