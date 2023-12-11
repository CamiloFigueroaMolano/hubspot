from django.contrib import admin
from django.urls import path, include

from hubspot_integration.views import list_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hubspot/', include('hubspot_integration.urls')),
    path('', list_users, name='list_users'),
]