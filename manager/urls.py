from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.APICreateView.as_view(), name='manager-create-api'),
    path('<str:pk>/', views.APIDetailView.as_view(), name='manager-api'),
    path('<str:pk>/update/', views.APIUpdateView.as_view(), name='manager-update-api'),
    path('<str:uid>/reset/', views.reset_api_view, name='manager-reset-api'),
    path('<str:pk>/delete/', views.DeleteAPIView.as_view(), name='manager-delete-api')
]
