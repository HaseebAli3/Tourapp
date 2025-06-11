from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer

class LocationListView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class LocationByNameView(APIView):
    def get(self, request, name):
        locations = Location.objects.filter(name__icontains=name)
        if not locations:
            return Response({"error": "No locations found"}, status=404)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)