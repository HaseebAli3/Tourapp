from rest_framework import serializers
from .models import Booking
from locations.serializers import LocationSerializer

class BookingSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Include full location details
    
    class Meta:
        model = Booking
        fields = ['id', 'location', 'booking_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['location', 'booking_date']  # Just need location ID and date for creation