# from django.contrib import admin
from django.urls import path , include 
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('website.urls', namespace='website')),
    path('api/', include('api.urls', namespace='api')),
    path('bettingapi/', include('bettingapi.urls', namespace='bettingapi')),
    path('admin/bettingapp/', include('bettingapp.urls', namespace='bettingapp')),
    path('admin/', include('dashboard.urls', namespace='dashboard'))
]
 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)