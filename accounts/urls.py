from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # include the default django auth urls
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
