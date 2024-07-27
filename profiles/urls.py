from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import MainPageView
from .views import MainPageApiView


urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('api/', MainPageApiView.as_view(), name='api/main_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    

