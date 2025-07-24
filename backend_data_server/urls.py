# ...existing code...
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("homepage/", include("backend_data_server.homepage.urls")),
]
# ...existing code...