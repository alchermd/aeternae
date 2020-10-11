from django.urls import path

from dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("", views.home, name="home"),
    path("sessions/", views.sessions, name="sessions"),
    path("revenue/", views.revenue, name="revenue"),
]
