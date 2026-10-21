
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from movies.models import EventSchedule, Seat

sides = ["top", "bottom", "left", "right"]

for schedule in EventSchedule.objects.all():
    created_count = 0

    for side in sides:
        for num in range(1, 21):
            seat_number = f"{side[0].upper()}{num:02d}"

            seat, created = Seat.objects.get_or_create(
                schedule=schedule,
                seat_number=seat_number,
                defaults={
                    "side": side,
                    "is_booked": False,
                },
            )

            if created:
                created_count += 1

            # Correct the side for existing seats with these new names.
            elif seat.side != side:
                seat.side = side
                seat.save(update_fields=["side"])

    print(
        f"Schedule {schedule.id}: "
        f"{schedule.seats.count()} seats total, "
        f"{created_count} newly created."
    )
