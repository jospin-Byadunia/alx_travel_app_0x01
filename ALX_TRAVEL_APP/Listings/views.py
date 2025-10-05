from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

##In listings/views.py, create viewsets for Listing and Booking using Django REST framework’s ModelViewSet.
##Ensure that these views provide CRUD operations for both models.

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'price', 'available_dates']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'created_at']
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['listing', 'user', 'booking_date']
    search_fields = ['listing__title', 'user__username']
    ordering_fields = ['booking_date', 'created_at']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()
    def perform_update(self, serializer):
        if self.request.user == serializer.instance.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this booking.")
    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this booking.")
##Implement filtering, searching, and ordering functionalities for both Listing and Booking views.
##Ensure that only authenticated users can create, update, or delete listings and bookings, while unauthenticated users can only read them.

