from django.urls import path
from . import views


urlpatterns = [
    path('<str:uid>/', views.execute_view, name='api-make-request'),
    path('<str:uid>/disable', views.disable_api_view, name='api-disable'),
    path('<str:uid>/enable', views.enable_api_view, name='api-enable'),
]
