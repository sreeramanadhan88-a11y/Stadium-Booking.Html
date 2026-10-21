
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)

from .models import (
    Event,
    Stadium,
    EventSchedule,
    Booking,
    Seat,
)

from .serializers import (
    EventSerializer,
    StadiumSerializer,
    EventScheduleSerializer,
    BookingSerializer,
    SeatSerializer,
)


# Event API
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # Support JSON data and image uploads
    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]


# Stadium API
class StadiumViewSet(viewsets.ModelViewSet):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer


# Event Schedule API
class EventScheduleViewSet(viewsets.ModelViewSet):
    queryset = EventSchedule.objects.all()
    serializer_class = EventScheduleSerializer

    @action(detail=True, methods=["get"])
    def seats(self, request, pk=None):
        schedule = self.get_object()

        # Create 80 seats only if this schedule has no seats
        if not schedule.seats.exists():
            sides = ["top", "bottom", "left", "right"]

            seats = [
                Seat(
                    schedule=schedule,
                    side=side,
                    seat_number=f"{side[0].upper()}{num:02d}",
                    is_booked=False,
                )
                for side in sides
                for num in range(1, 21)
            ]

            Seat.objects.bulk_create(seats)

        # Return seats ordered by side and seat number
        seats = schedule.seats.all().order_by(
            "side", "seat_number"
        )

        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


# Booking API
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()

        # Mark selected seats as booked
        seat_numbers = [
            seat.strip()
            for seat in booking.selected_seats.split(",")
        ]

        Seat.objects.filter(
            schedule=booking.schedule,
            seat_number__in=seat_numbers,
        ).update(is_booked=True)
