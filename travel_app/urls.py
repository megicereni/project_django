from django.urls import path
from django.urls import path
from django.contrib.auth.views import LogoutView

from travel_app import views

from travel_app import views
from travel_app.views import ResponseMessageView, BookingDetailView, CustomLoginView, register_view, \
    subscribe_newsletter, send_newsletter

urlpatterns = [
    # Home page uses the same package list view.
    path('', views.GeneralPackageListView.as_view(), name='home'),

    # List/search page:
    # /packages/
    # /packages/?q=Paris
    path('packages/', views.GeneralPackageListView.as_view(), name='package_list'),

    # Old template links used "manage_package", so this name still points to the list.
    path('packages/', views.GeneralPackageListView.as_view(), name='manage_package'),

    # Create page for a new general package.
    path('packages/create/', views.GeneralPackageCreateView.as_view(), name='package_create'),

    # Detail page for one package. Django passes the id as "pk" to DetailView.
    path('packages/<int:pk>/', views.GeneralPackageDetailView.as_view(), name='package_detail'),

    # Edit page for one package. Django passes the id as "pk" to UpdateView.
    path('packages/<int:pk>/edit/', views.GeneralPackageUpdateView.as_view(), name='package_edit'),

    # Delete action for one package. This should be used with POST, not a normal link.
    path('packages/<int:pk>/delete/', views.GeneralPackageDeleteView.as_view(), name='package_delete'),

    path('attractions/', views.AttractionCreateView.as_view(), name='attraction_create'),

    path('custom/<int:pk>/create', views.CustomPackageCreateView.as_view(), name='custom_create'),

    path('custom/<int:pk>/edit/', views.CustomPackageUpdateView.as_view(), name='custom_edit'),

    path('bookings/list', views.BookingListView.as_view(), name='booking_list'),

    path('booking/<int:pk>/confirm', views.confirm_booking, name='booking_confirm'),
    path('booking/<int:pk>/cancel', views.cancel_booking, name='booking_cancel'),

    path('messages/list', views.MessageListView.as_view(), name='message_list'),

    path("message/<int:pk>/reply/", ResponseMessageView.as_view(), name="message_reply"),

    path("booking/<int:pk>/", BookingDetailView.as_view(), name="booking_detail"),

    path('reviews/', views.ReviewListView.as_view(), name='review_list'),

    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),

    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_edit'),

    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),

    path('payments/list', views.PaymentListView.as_view(), name='payment_list'),

    path("my-messages/", views.ClientMessageListView.as_view(), name="client_message_list"),

    path("my-messages/create/", views.ClientMessageCreateView.as_view(), name="client_message_create"),

    path("booking/create/<int:pk>/", views.ClientBookingCreateView.as_view(), name="booking_create"),

    path("my-bookings/", views.ClientBookingListView.as_view(), name="my_bookings"),

    path("my-bookings/<int:pk>/cancel/", views.ClientBookingCancelView.as_view(), name="client_booking_cancel"),
    path('client/package/<int:pk>/', views.ClientPackageDetailView.as_view(), name='client_package_detail'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("newsletter/subscribe/", subscribe_newsletter, name="newsletter_subscribe"),
    path("newsletter/send/", send_newsletter, name="send_newsletter"),

]
