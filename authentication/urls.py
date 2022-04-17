from django.urls import path
from authentication import views as auth_views

urlpatterns = [
    path("allow-calender-access/" , auth_views.GoogleCalendarinitView , name = "allow-calender-access") ,
    path("get-calender-access/<int:user_id>" , auth_views.GoogleCalendarRedirectView , name = "get-calender-access") ,
]   