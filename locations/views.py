from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer

# 1. List all Locations
class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# 2. List Locations by Name (custom filter with generic view)
class LocationByNameView(generics.ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Location.objects.filter(name__icontains=name)
