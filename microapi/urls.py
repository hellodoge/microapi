from django.contrib import admin
from django.urls import path, include
from manager.views import APIListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('manage/', include('manager.urls')),
    path('', APIListView.as_view(), name='manager-home')
]
