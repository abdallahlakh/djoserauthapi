from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('', include('account.urls2')),
    path('adi/', include('mouhami_api.urls')),
]

