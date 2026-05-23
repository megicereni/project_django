from datetime import timezone

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import GeneralPackageForm, CustomPackageForm, AttractionForm, MessageForm, ReviewForm
from .models import GeneralPackages, CustomPackages, Review, Attraction, PackagesAttraction, Booking, Payment, Message


class StaffRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class GeneralPackageCreateView(StaffRequiredMixin, CreateView):
    model = GeneralPackages
    form_class = GeneralPackageForm

    # template_name=
    def form_valid(self, form):
        response = super().form_valid(form)
        package = self.object

        days = self.request.POST.getlist('day[]')
        attractions = self.request.POST.getlist('attraction[]')

        for day, attraction_id in zip(days, attractions):
            if day and attraction_id:
                PackagesAttraction.objects.create(
                    package=package,
                    attraction_id=attraction_id,
                    day=day
                )

        messages.success(self.request, "Successfully created package")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Package is not created successfully")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class CustomPackageCreateView(StaffRequiredMixin, CreateView):
    model = CustomPackages
    form_class = CustomPackageForm

    # template_name=
    def dispatch(self, request, *args, **kwargs):
        self.general_packages_id = kwargs['pk']
        self.package = GeneralPackages.objects.get(pk=self.general_packages_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Successfully created package")
        return response

    def get_success_url(self):
        return reverse_lazy('packages_list')


class CustomPackageUpdateView(StaffRequiredMixin, UpdateView):
    model = CustomPackages
    form_class = CustomPackageForm


class GeneralPackageDeleteView(StaffRequiredMixin, DeleteView):
    model = GeneralPackages

    def get_success_url(self):
        messages.success(self.request, "Successfully deleted package")
        return reverse_lazy('packages_list')


class AttractionCreateView(StaffRequiredMixin, CreateView):
    model = Attraction
    form_class = AttractionForm
    def get_success_url(self):
        messages.success(self.request, "Successfully deleted package")
        return reverse_lazy('manage_packages')



def add_itinerary(request, package_pk):
    package = get_object_or_404(GeneralPackages, pk=package_pk)
    days = request.POST.getlist('day[]')
    attractions = request.POST.getlist('attraction[]')
    for day, attraction_id in zip(days, attractions):
        if day and attraction_id: PackagesAttraction.objects.create( package=package, attraction_id=attraction_id, day=day )
        return redirect('package_detail', pk=package.pk)


class BookingListView(ListView):
    model = Booking
    context_object_name = 'bookings'
    # template_name=
    ordering = ['-created_at']


class PaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'
    ordering = ['-created_at']


#     template_name=


@login_required
def book_package(request, pk):
    package = get_object_or_404(CustomPackages, pk=pk)

    existing = Booking.objects.filter(user=request.user, package=package).first()
    if existing:
        messages.warning(request, 'You have already booked this package.')
        return redirect('my_bookings')

    if request.method == 'POST':
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            status='pending'
        )
        # Create Payment linked to this booking
        Payment.objects.create(
            booking=booking,
            totalPrice=package.price,
            refundedAmount=0
        )
        messages.success(request, 'Booking completed! Payment is due within 24 hours.')
        return redirect('my_bookings')

    return render(request, 'travel_app/book_confirm.html', {'package': package})


@login_required
def my_bookings(request):
    bookings = (Booking.objects.filter(
        user=request.user
    ).select_related('package', 'payment').order_by('-created_at'))
    return render(request, 'travel_app/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status != 'approved':
        messages.error(request, 'Only approved bookings can be cancelled.')
        return redirect('my_bookings')

    if request.method == 'POST':
        payment = Payment.objects.filter(booking=booking).first()
        if payment:
            payment.refundedAmount = 0.5 * booking.totalPrice
            payment.save()
        booking.status = 'canceled'
        booking.save()
        messages.success(request, 'Booking cancelled. A 50% refund will be processed.')
        return redirect('my_bookings')

    return render(request, 'travel_app/cancel_confirm.html', {'booking': booking})

def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.numberOfPeople > booking.package.limitNumberOfPeople:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, "It can be overbooking")
    booking.status = 'approved'
    booking.save()
    return redirect('bookings_list')


def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'canceled'
    booking.save()


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



@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'travel_app/my_reviews.html', {'reviews': reviews})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):

        form.instance.user = self.request.user

        response = super().form_valid(form)

        messages.success(self.request, "Successfully created review")

        return response

    def form_invalid(self, form):

        messages.error(self.request, "Review is not created successfully")

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy('home')


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(self.request, "Successfully updated review")

        return response

    def form_invalid(self, form):

        messages.error(self.request, "Review is not updated successfully")

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy('home')


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review

    def get_success_url(self):

        messages.success(self.request, "Successfully deleted review")

        return reverse_lazy('home')
# ── MESAZHET ────────────────────────────────────────────
@login_required
def my_messages(request):
    user_messages = Message.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'travel_app/my_messages.html', {'messages_list': user_messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.name = request.user.get_full_name() or request.user.username
            msg.email = request.user.email
            msg.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('my_messages')
    else:
        form = MessageForm(initial={
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        })

    return render(request, 'travel_app/send_message.html', {'form': form})
#per review te userit te loguar
class ReviewListView(LoginRequiredMixin, ListView):

    model = Review

    template_name = 'review/review_list.html'

    context_object_name = 'reviews'

    def get_queryset(self):

        return Review.objects.filter(
            user=self.request.user
        )
