from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('quiz.urls', namespace='quiz')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('nested_admin/', include('nested_admin.urls')),
]
