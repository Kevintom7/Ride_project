from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rides_app.models import Ride
from .serializers import RideSerializer
from django.db import models

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)


    def get_queryset(self):
        user = self.request.user

        if user.role == 'driver':
            return Ride.objects.filter(
                models.Q(status='requested') | models.Q(driver=user)
            )

        return Ride.objects.filter(rider=user)


    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        ride = self.get_object()
        user = request.user

        if not hasattr(user, 'role') or user.role != 'driver':
            return Response(
                {"error": "Only drivers can accept rides"},
                status=status.HTTP_403_FORBIDDEN
            )

        if ride.status != 'requested':
            return Response(
                {"error": f"Ride already {ride.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.driver = user
        ride.status = 'accepted'
        ride.save()

        return Response({
            "message": "Ride accepted",
            "ride_id": ride.id,
            "status": ride.status
        })


    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get('status')


        valid_statuses = [choice[0] for choice in Ride.Status.choices]
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=400)


        if ride.status == 'completed':
            return Response({"error": "Ride already completed"}, status=400)

        if ride.status == 'cancelled':
            return Response({"error": "Ride cancelled"}, status=400)

        # DRIVER PERMISSION CHECK
        if new_status in ['started', 'completed'] and request.user != ride.driver:
            return Response({"error": "Only driver allowed"}, status=403)

        # UPDATE STATUS
        ride.status = new_status
        ride.save()

        return Response({
            "message": f"Ride {new_status}",
            "status": ride.status
        })

    #  REAL-TIME LOCATION UPDATE
    @action(detail=True, methods=['POST'])
    def update_location(self, request, pk=None):
        ride = self.get_object()

        # ADD HERE (ONLY DRIVER CAN UPDATE)
        if request.user != ride.driver:
            return Response(
                {"error": "Only driver can update location"},
                status=403
            )

        lat = request.data.get('current_lat')
        lng = request.data.get('current_lng')

        #  validation
        if lat is None or lng is None:
            return Response(
                {"error": "Latitude and Longitude required"},
                status=400
            )

        try:
            ride.current_lat = float(lat)
            ride.current_lng = float(lng)
        except ValueError:
            return Response(
                {"error": "Invalid latitude/longitude"},
                status=400
            )

        ride.save()

        return Response({
            "message": "Location updated successfully",
            "current_lat": ride.current_lat,
            "current_lng": ride.current_lng
        })