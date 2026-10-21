
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    banner = models.ImageField(
        upload_to='event_banners/',
        blank=True,
        null=True
    )
    category = models.CharField(max_length=100)
    artists_or_teams = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Stadium(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=250)
    total_capacity = models.IntegerField(default=40000)

    def __str__(self):
        return f"{self.name} - {self.location}"


class EventSchedule(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    stadium = models.ForeignKey(
        Stadium,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    start_time = models.DateTimeField()
    vip_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=2500.00
    )
    regular_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=500.00
    )

    def __str__(self):
        return f"{self.event.title} at {self.stadium.name}"


def save(self, *args, **kwargs):
    is_new = self.pk is None
    super().save(*args, **kwargs)

    if is_new:
        sides = ['top', 'bottom', 'left', 'right']

        seats = [
            Seat(
                schedule=self,
                side=side,
                seat_number=f"{side[0].upper()}{num:02d}",
                is_booked=False
            )
            for side in sides
            for num in range(1, 21)
        ]

        Seat.objects.bulk_create(seats)


class Booking(models.Model):
    schedule = models.ForeignKey(
        EventSchedule,
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=150)
    seat_category = models.CharField(max_length=50)
    selected_seats = models.CharField(max_length=250)
    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Booking {self.id} - {self.customer_name} "
            f"({self.selected_seats})"
        )


class Seat(models.Model):
    SIDE_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('left', 'Left'),
        ('right', 'Right'),
    ]

    schedule = models.ForeignKey(
        EventSchedule,
        on_delete=models.CASCADE,
        related_name='seats'
    )
    side = models.CharField(
        max_length=10,
        choices=SIDE_CHOICES
    )
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['schedule', 'seat_number'],
                name='unique_seat_per_schedule'
            )
        ]

    def __str__(self):
        return (
            f"{self.side.title()} - {self.seat_number} "
            f"({'Booked' if self.is_booked else 'Available'})"
        )
