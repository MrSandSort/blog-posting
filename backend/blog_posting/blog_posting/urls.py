
from django.contrib import admin
from django.urls import path, include
from . import accounts 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts.urls))
]
