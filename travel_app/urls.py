from django.urls import path

from travel_app import views

urlpatterns = [
    path('', views.GeneralPackageCreateView.as_view(), name='home'),
    ]