
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('grievances/', include('grievances.urls')),
]
