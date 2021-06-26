from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('getRef.urls'), name='getref'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]