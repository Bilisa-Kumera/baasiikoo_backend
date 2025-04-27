from django.contrib import admin
from django.urls import path, include
from expenses.views import home

urlpatterns = [
    path('', home, name='home'),          
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),
]
