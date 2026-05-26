from django.urls import path

from travel_app import views

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

    path('attractions/',views.AttractionCreateView.as_view(), name='attraction_create'),

    path('custom/<int:pk>/create',views.CustomPackageCreateView.as_view(), name='custom_create'),

    path('custom/<int:pk>/edit/',views.CustomPackageUpdateView.as_view(), name='custom_edit'),

    path('bookings/list',views.BookingListView.as_view(), name='booking_list'),

    path('booking/<int:pk>/confirm',views.confirm_booking, name='booking_confirm'),
    path('booking/<int:pk>/cancel',views.cancel_booking, name='booking_cancel'),
    path('booking/<int:pk>/refund',views.refund_booking, name='booking_refund'),

    ]