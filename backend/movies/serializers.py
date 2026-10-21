from rest_framework import serializers
from .models import Event, Stadium, EventSchedule, Booking,Seat

class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'

class EventScheduleSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
    stadium_id = serializers.PrimaryKeyRelatedField(
        queryset=Stadium.objects.all(), source='stadium', write_only=True
    )

    class Meta:
        model = EventSchedule
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    schedules = EventScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = [
            'id',
            'schedule',
            'side',
            'seat_number',
            'is_booked'
        ]
