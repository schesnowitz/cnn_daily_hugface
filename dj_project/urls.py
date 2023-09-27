
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('raw_data.urls', namespace='raw_data')),
    path('cnn-daily', include('cnn_daily.urls', namespace='cnn_daily')),
]
