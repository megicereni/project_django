from datetime import timezone
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import GeneralPackageForm, CustomPackageForm, AttractionForm, ReviewForm, ResponseMessageForm,LoginForm, RegisterForm
from .models import GeneralPackages, CustomPackages, Review, Attraction, PackagesAttraction, Booking, Payment, Message


class StaffRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_staff

class GeneralPackageListView(ListView):
    model = GeneralPackages
    template_name = "admin/package_list.html"
    context_object_name = "packages"
    ordering = ["-id"]

    def get_queryset(self):
        # Start with the normal queryset from ListView:
        # GeneralPackages.objects.all().order_by("-id")
        queryset = super().get_queryset()

        # Read the search text from the URL query string.
        # Example: /packages/?q=Paris
        search = self.request.GET.get("q", "").strip()

        # If the user typed something, filter by title, destination, or description.
        # Q objects let us use OR conditions in Django queries.
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(destination__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        # Add the search text back to the template so the input keeps its value
        # after the page refreshes.
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "").strip()
        return context
class GeneralPackageDetailView(DetailView):
    model = GeneralPackages
    template_name = "admin/package_detail.html"
    context_object_name = "package"

    def get_context_data(self, **kwargs):
        # The main package is already available as "package".
        # Here we add its itinerary rows from the through model PackagesAttraction.
        context = super().get_context_data(**kwargs)
        context["itinerary"] = PackagesAttraction.objects.filter(
            package=self.object
        ).select_related("attraction").order_by("day")
        context["custom_packages"] = CustomPackages.objects.filter(
            package=self.object
        ).order_by("departureDate")
        return context

class BookingDetailView(DetailView):
    model = Booking
    template_name = "admin/booking_detail.html"
    context_object_name = "booking"

class GeneralPackageFormMixin:
    model = GeneralPackages
    form_class = GeneralPackageForm
    template_name = "admin/package_form.html"

    def save_itinerary(self, package):
        # The HTML form sends many "day" values and many "attraction" values.
        # getlist() returns all of them as Python lists.
        days = self.request.POST.getlist("day")
        attractions = self.request.POST.getlist("attraction")

        # When editing, remove old itinerary rows first.
        # Then we recreate the rows from the submitted form values.
        PackagesAttraction.objects.filter(package=package).delete()

        # zip() pairs each day with the attraction selected on the same row.
        # Empty rows are skipped so students/users can leave the last row blank.
        for day, attraction_id in zip(days, attractions):
            if not day or not attraction_id:
                continue
            PackagesAttraction.objects.create(
                package=package,
                attraction_id=attraction_id,
                day=day
            )

    def get_context_data(self, **kwargs):
        # The form template needs all attractions so it can build the dropdown.
        context = super().get_context_data(**kwargs)
        context["attractions"] = Attraction.objects.all()

        # self.object exists when editing, but it is None when creating.
        # For edit pages, send the existing itinerary so the form is pre-filled.
        if self.object:
            context["itinerary"] = PackagesAttraction.objects.filter(
                package=self.object
            ).select_related("attraction").order_by("day")
        return context

class GeneralPackageCreateView(GeneralPackageFormMixin, CreateView):
    def form_valid(self, form):
        # First let Django save the GeneralPackages object.
        response = super().form_valid(form)

        # Then save the itinerary rows connected to that new package.
        self.save_itinerary(self.object)
        messages.success(self.request, "Successfully created package")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Package is not created successfully")
        return super().form_invalid(form)

    def get_success_url(self):
        # After creating, send the user to the detail page for the new package.
        return reverse_lazy('package_detail', kwargs={'pk': self.object.pk})

class GeneralPackageUpdateView(GeneralPackageFormMixin, UpdateView):
    def form_valid(self, form):
        # Save changes to the main package fields first.
        response = super().form_valid(form)

        # Then replace the old itinerary rows with the submitted rows.
        self.save_itinerary(self.object)
        messages.success(self.request, "Successfully updated package")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Package is not updated successfully")
        return super().form_invalid(form)

    def get_success_url(self):
        # After editing, return to the same package's detail page.
        return reverse_lazy('package_detail', kwargs={'pk': self.object.pk})

class GeneralPackageDeleteView(DeleteView):
    model = GeneralPackages

    def get_success_url(self):
        messages.success(self.request, "Successfully deleted package")
        return reverse_lazy('package_list')

class CustomPackageCreateView(CreateView):
    model = CustomPackages
    form_class = CustomPackageForm
    template_name="admin/custom_package.html"
    def dispatch(self, request, *args, **kwargs):
        self.package = GeneralPackages.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general'] = self.package
        return context
    def form_valid(self, form):
        form.instance.package = self.package
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('package_list')


class CustomPackageUpdateView(UpdateView):
    model = CustomPackages
    form_class = CustomPackageForm
    template_name = "admin/custom_package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general'] = self.object.package  # lidhja ekzistuese
        return context

    def get_success_url(self):
        return reverse_lazy('package_detail', kwargs={'pk': self.object.pk})


#
class AttractionCreateView(CreateView):
    model = Attraction
    form_class = AttractionForm
    template_name = "admin/attraction.html"
    def get_success_url(self):
        messages.success(self.request, "Successfully deleted package")
        return reverse_lazy('package_list')

class ResponseMessageView(UpdateView):
    model = Message
    form_class = ResponseMessageForm
    template_name = "admin/reply_message.html"

    def form_valid(self, form):
        messages.success(self.request, "Reply sent successfully")

        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('package_list')

class BookingListView(ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name="admin/booking_list.html"
    ordering = ['-created_at']
class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name="admin/messages_list.html"
    ordering = ['-id']

#
# class PaymentListView(ListView):
#     model = Payment
#     context_object_name = 'payments'
#     ordering = ['-created_at']
#     template_name="admin/payment_list.html"
#
# @login_required
# def book_package(request, pk):
#     package = get_object_or_404(CustomPackages, pk=pk)
#
#     existing = Booking.objects.filter(user=request.user, package=package).first()
#     if existing:
#         messages.warning(request, 'You have already booked this package.')
#         return redirect('my_bookings')
#
#     if request.method == 'POST':
#         booking = Booking.objects.create(
#             user=request.user,
#             package=package,
#             status='pending'
#         )
#         # Create Payment linked to this booking
#         Payment.objects.create(
#             booking=booking,
#             totalPrice=package.price,
#             refundedAmount=0
#         )
#         messages.success(request, 'Booking completed! Payment is due within 24 hours.')
#         return redirect('my_bookings')
#
#     return render(request, 'travel_app/book_confirm.html', {'package': package})
#
#
# @login_required
# def my_bookings(request):
#     bookings = (Booking.objects.filter(
#         user=request.user
#     ).select_related('package', 'payment').order_by('-created_at'))
#     return render(request, 'travel_app/my_bookings.html', {'bookings': bookings})
#
# @login_required
# def cancel_booking(request, pk):
#     booking = get_object_or_404(Booking, pk=pk, user=request.user)
#
#     if booking.status != 'approved':
#         messages.error(request, 'Only approved bookings can be cancelled.')
#         return redirect('my_bookings')
#
#     if request.method == 'POST':
#         payment = Payment.objects.filter(booking=booking).first()
#         if payment:
#             payment.refundedAmount = 0.5 * booking.totalPrice
#             payment.save()
#         booking.status = 'canceled'
#         booking.save()
#         messages.success(request, 'Booking cancelled. A 50% refund will be processed.')
#         return redirect('my_bookings')
#
#     return render(request, 'travel_app/cancel_confirm.html', {'booking': booking})
#
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.numberOfPeople > booking.package.limitNumberOfPeople:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, "It can be overbooking")
    booking.status = 'approved'
    booking.save()
    return redirect('booking_list')
#
#
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'canceled'
    booking.save()
    return redirect('booking_list')
#
#
def refund_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    payment = get_object_or_404(Payment, booking=booking)
    date = booking.package.departureDate
    now = timezone.now().date()
    diff = (date - now).days
    if booking.status == 'approved' and diff <= 1:
        payment.refundedAmount = 0
        booking.status = 'canceled'
        booking.save()
    elif booking.status == 'approved' and diff >= 15:
        payment.refundedAmount = 0.5 * booking.totalPrice
        booking.status = 'refunded'
        booking.save()
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "client/review_list.html"
    context_object_name = "reviews"
    ordering = ["-id"]

    def get_queryset(self):
        return Review.objects.filter(
            booking__client=self.request.user
        ).select_related("booking", "booking__package").order_by("-id")


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "client/review_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["booking"].queryset = Booking.objects.filter(
            client=self.request.user,
            status="approved"
        )

        return form

    def form_valid(self, form):
        booking = form.cleaned_data["booking"]

        if booking.client != self.request.user:
            messages.error(self.request, "You cannot review this booking")
            return self.form_invalid(form)

        response = super().form_valid(form)

        messages.success(self.request, "Successfully created review")

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Review is not created successfully")

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("review_list")


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "client/review_form.html"

    def get_queryset(self):
        return Review.objects.filter(
            booking__client=self.request.user
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["booking"].queryset = Booking.objects.filter(
            client=self.request.user,
            status="approved"
        )

        return form

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(self.request, "Successfully updated review")

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Review is not updated successfully")

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("review_list")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "client/review_confirm_delete.html"

    def get_queryset(self):
        return Review.objects.filter(
            booking__client=self.request.user
        )

    def get_success_url(self):
        messages.success(self.request, "Successfully deleted review")

        return reverse_lazy("review_list")
