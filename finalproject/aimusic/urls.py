from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'aimusic'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload_complete/', views.upload_complete, name='upload_complete'),
    path('music/', views.music, name='music')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
