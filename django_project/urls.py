from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('card/', include('card.urls')),
    path('accounts/', include('users.urls')),

]
