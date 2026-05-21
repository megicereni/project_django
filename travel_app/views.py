from datetime import timezone

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import GeneralPackageForm, CustomPackageForm, AttractionForm, PackageAttractionForm, MessageForm, ReviewForm
from .models import GeneralPackages, CustomPackages, Review, Attraction, PackagesAttraction, Booking, Payment, Message

Message


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


class PackageAttractionCreateView(StaffRequiredMixin, CreateView):
    model = PackagesAttraction
    form_class = PackageAttractionForm

    def dispatch(self, request, *args, **kwargs):
        self.package = get_object_or_404(GeneralPackages, pk=kwargs['package_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.package_id = self.kwargs['package_pk']
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['attraction'].queryset = Attraction.objects.all()
        return form


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


@login_required
def add_review(request, package_pk):
    package = get_object_or_404(CustomPackages, pk=package_pk)

    # Check if user has an approved booking for this package
    has_confirmed = Booking.objects.filter(
        user=request.user, package=package, status='approved'
    ).exists()
    if not has_confirmed:
        messages.error(request, 'You must have an approved booking to leave a review.')
        return redirect('package_detail', pk=package_pk)

    # Check if user already left a review
    already_reviewed = Review.objects.filter(user=request.user, package=package).exists()
    if already_reviewed:
        messages.warning(request, 'You have already reviewed this package.')
        return redirect('package_detail', pk=package_pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.package = package
            review.save()
            messages.success(request, 'Review posted successfully!')
            return redirect('package_detail', pk=package_pk)
    else:
        # Pre-fill fields from logged-in user
        form = ReviewForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'travel_app/review_form.html', {'form': form, 'package': package})


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('my_reviews')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'travel_app/review_form.html', {'form': form, 'package': review.package})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('my_reviews')
    return render(request, 'travel_app/review_delete_confirm.html', {'review': review})


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