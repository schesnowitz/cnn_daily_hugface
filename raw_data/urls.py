
from django.urls import path, include
from . views import index
app_name='raw_data'
urlpatterns = [

    path('', index, name='index'),
]
