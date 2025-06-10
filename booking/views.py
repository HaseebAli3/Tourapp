from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer, CreateBookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    
    def get_serializer_class(self):
        return CreateBookingSerializer if self.request.method == 'POST' else BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('location')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDeleteView(generics.DestroyAPIView):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)