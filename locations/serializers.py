from rest_framework import serializers
from .models import Location, LocationImage

class LocationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'price', 'location_url', 'images']
    
    def get_images(self, obj):
        return [img.image.url for img in obj.images.all()]