from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, StadiumViewSet, EventScheduleViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'stadiums', StadiumViewSet)
router.register(r'schedules', EventScheduleViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]