from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  LocationListView, LocationByNameView

urlpatterns = [
    path('list/', LocationListView.as_view(), name='location-list'),
    path('get/<str:name>/', LocationByNameView.as_view(), name='location-by-name'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)