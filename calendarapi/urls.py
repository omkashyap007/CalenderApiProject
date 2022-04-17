from django.urls import path
from calendarapi import views as api_views

urlpatterns = [
    path("calendar/init/" , api_views.calendarInit , name = "api-calendar-init"),
    path("calendar/redirect/" , api_views.calendarRedirect , name = "api-calendar-redirect")
]