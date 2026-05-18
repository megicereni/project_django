from datetime import timezone

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import GeneralPackageForm, CustomPackageForm, AttractionForm, PackageAttractionForm
from .models import GeneralPackages, CustomPackages, Review, Attraction, PackagesAttraction, Booking, Payment


class StaffRequiredMixin(UserPassesTestMixin,LoginRequiredMixin):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_staff

class GeneralPackageCreateView(StaffRequiredMixin,CreateView):
    model=GeneralPackages
    form_class = GeneralPackageForm
    # template_name=
    def form_valid(self,form):
        response=super().form_valid(form)
        messages.success(self.request,"Successfully created package")
        return response
    def form_invalid(self,form):
        messages.error(self.request,"Package is not created successfully")
        return super().form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('home')

class CustomPackageCreateView(StaffRequiredMixin,CreateView):
    model=CustomPackages
    form_class = CustomPackageForm
    # template_name=
    def dispatch(self, request, *args, **kwargs):
        self.general_packages_id=kwargs['pk']
        self.package=GeneralPackages.objects.get(pk=self.general_packages_id)
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self,form):
        response=super().form_valid(form)
        messages.success(self.request,"Successfully created package")
        return response
    def get_success_url(self):
        return reverse_lazy('packages_list')

class CustomPackageUpdateView(StaffRequiredMixin,UpdateView):
    model=CustomPackages
    form_class = CustomPackageForm
class GeneralPackageDeleteView(StaffRequiredMixin,DeleteView):
    model=GeneralPackages
    def get_success_url(self):
        messages.success(self.request,"Successfully deleted package")
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

def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.numberOfPeople>booking.package.limitNumberOfPeople:
        booking.status = 'canceled'
        booking.save()
        messages.success(request,"It can be overbooking")
    booking.status = 'approved'
    booking.save()
    return redirect('bookings_list')
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status='canceled'
    booking.save()
def refund_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    payment=get_object_or_404(Payment, booking=booking)
    date=booking.package.departureDate
    now=timezone.now().date()
    diff=(date-now).days
    if booking.status=='approved' and diff<=1:
        payment.refundedAmount=0
        booking.status = 'canceled'
        booking.save()
    elif booking.status=='approved' and diff>=15:
        payment.refundedAmount=0.5 * booking.totalPrice
        booking.status = 'refunded'
        booking.save()
