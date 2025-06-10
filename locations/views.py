from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer
from django.shortcuts import get_list_or_404


# -----------------------------
# 1. List all locations (Authenticated users)
# -----------------------------
class LocationListView(APIView):
  
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

# -----------------------------
# 2. Get single location by name (Authenticated users)
# -----------------------------
class LocationByNameView(APIView):
    
    def get(self, request, name):
        # Use icontains for partial and case-insensitive match
        locations = get_list_or_404(Location, name__icontains=name)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)