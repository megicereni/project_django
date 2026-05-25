"""
URL configuration for travel_agency_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from travel_app.views import (
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewListView,
)
from travel_app.views import (
    BookingCreateView,
    BookingListView,
    CancelBookingView,
    RefundBookingView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
]
path(
    'review/create/<int:pk>/',
    ReviewCreateView.as_view(),
    name='review_create'
),

path(
    'review/update/<int:pk>/',
    ReviewUpdateView.as_view(),
    name='review_update'
),

path(
    'review/delete/<int:pk>/',
    ReviewDeleteView.as_view(),
    name='review_delete'
),

urlpatterns = [

    path(
        'booking/create/',
        BookingCreateView.as_view(),
        name='booking_create'
    ),

    path(
        'booking/list/',
        BookingListView.as_view(),
        name='booking_list'
    ),

    path(
        'booking/cancel/<int:pk>/',
        CancelBookingView.as_view(),
        name='booking_cancel'
    ),

    path(
        'booking/refund/<int:pk>/',
        RefundBookingView.as_view(),
        name='booking_refund'
    ),
]