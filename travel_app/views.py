import os
from datetime import timezone, timedelta

from django.core.mail import send_mass_mail, EmailMultiAlternatives
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import GeneralPackageForm, CustomPackageForm, AttractionForm, ReviewForm, ResponseMessageForm, BookingForm, \
    RegisterForm, LoginForm, NewsletterForm
from .forms import MessageForm
from .models import GeneralPackages, CustomPackages, Review, Attraction, PackagesAttraction, Booking, Payment, Message, \
     NewsletterSubscriber
from travel_app.models import GeneralPackages, CustomPackages, Attraction, PackagesAttraction, Booking, Message, Review, \
    Client
from django import forms


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
    template_name = "admin/custom_package.html"

    def dispatch(self, request, *args, **kwargs):
        self.package = GeneralPackages.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general'] = self.package
        return context

    def form_valid(self, form):
        form.instance.package = self.package
        departure = form.cleaned_data['departureDate']
        form.instance.arrivalDate = departure + timedelta(days=self.package.days)

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


class AttractionCreateView(CreateView):
    model = Attraction
    form_class = AttractionForm
    template_name = "admin/attraction.html"

    def get_success_url(self):
        messages.success(self.request, "Successfully added attraction")
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
    template_name = "admin/booking_list.html"
    ordering = ['-created_at']


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = "admin/messages_list.html"
    ordering = ['-id']


class PaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'
    ordering = ['-created_at']
    template_name = "admin/payment_list.html"


def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.numberOfPeople > booking.package.limitNumberOfPeople:
        booking.status = 'rejected'
        booking.save()
        messages.success(request, "It can be overbooking")
    booking.status = 'approved'
    booking.save()
    return redirect('booking_list')

def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    booking.status = 'rejected'
    booking.save()

    payment = booking.payment_set.first()

    if payment:
        payment.refundedAmount = booking.totalPrice
        payment.save()

    return redirect('booking_list')



# Kjo view shfaq listën e të gjitha paketave turistike që mund të shihen nga klientët.
class ClientPackageListView(ListView):
    # Modeli nga ku merren të dhënat
    model = GeneralPackages
    # Template që do të shfaqë paketat
    template_name = "client/package_list.html"
    # Emri që përdoret në template për listën e paketave
    context_object_name = "packages"
    # Paketat shfaqen nga më e reja tek më e vjetra
    ordering = ["-id"]

# Kjo view përdoret që klienti të krijojë një rezervim.
# LoginRequiredMixin siguron që vetëm përdoruesit e loguar
# mund të bëjnë rezervime.

class ClientBookingCreateView(LoginRequiredMixin, CreateView):
    # Modeli që do të ruhet në databazë
    model = Booking
    # Forma që përdoret për rezervimin
    form_class = BookingForm
    # Template që shfaq formularin
    template_name = "client/booking_form.html"

    # Merr paketën specifike që klienti dëshiron të rezervojë.
    # Nëse nuk ekziston, shfaqet gabimi 404.
    def dispatch(self, request, *args, **kwargs):
        self.package = get_object_or_404(CustomPackages, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    # Kjo metodë ekzekutohet kur forma plotësohet saktë.
    def form_valid(self, form):
        # Merr numrin e personave nga forma.
        number_of_people = form.cleaned_data["numberOfPeople"]
        # Kontrollon nëse numri i personave
        # kalon limitin e paketës.
        if number_of_people > self.package.limitNumberOfPeople:
            form.add_error(
                "numberOfPeople",
                "Number of people exceeds the package limit."
            )
            return self.form_invalid(form)
        # Krijon objektin Booking pa e ruajtur ende.
        booking = form.save(commit=False)
        booking.client = self.request.user# Vendos klientin aktual.
        booking.package = self.package #paketën e zgjedhur.
        # Ruan numrin e personave.
        booking.numberOfPeople = number_of_people
        # Llogarit çmimin total.
        booking.totalPrice = self.package.price * number_of_people
        booking.status = "pending" # Statusi fillestar është pending.
        booking.save()# Ruan rezervimin në databazë.
        # Krijon pagesën për rezervimin.
        Payment.objects.create(
            booking=booking,
            amount=booking.totalPrice,
            refundedAmount=0
        )

        messages.success(
            self.request,
            "Booking created successfully. Payment completed."
        )

        return redirect("my_bookings")

    # Ekzekutohet kur forma ka gabime.
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Booking was not created successfully."
        )
        return super().form_invalid(form)

    # Dërgon paketën në template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["package"] = self.package
        return context

# Shfaq të gjitha rezervimet e klientit të loguar.
class ClientBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "client/my_bookings.html"
    context_object_name = "bookings"

    # Merr vetëm rezervimet e klientit aktual.
    def get_queryset(self):
        return Booking.objects.filter(
            client=self.request.user
        ).select_related(
            "package",
            "package__package"
        ).order_by("-created_at")

# Lejon klientin të anulojë rezervimin.
class ClientBookingCancelView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = []
    template_name = "client/cancel_booking.html"

    # Klienti mund të anulojë vetëm rezervimet e tij.
    def get_queryset(self):
        return Booking.objects.filter(
            client=self.request.user
        )

    def form_valid(self, form):
        booking = self.object

        payment = booking.payment_set.first()

        if booking.status != "approved":
            messages.error(
                self.request,
                "Only approved bookings can be cancelled."
            )
            return redirect("my_bookings")

        diff = (
            booking.package.departureDate
            - timezone.now().date()
        ).days

        if payment:

            if diff >= 15:
                payment.refundedAmount = (
                    booking.totalPrice * 0.5
                )

            else:
                payment.refundedAmount = 0

            payment.save()

        booking.status = "rejected"
        booking.save()

        messages.success(
            self.request,
            "Booking cancelled successfully."
        )

        return redirect("my_bookings")

# Kjo view shfaq detajet e një pakete të përgjithshme për klientin.
class ClientPackageDetailView(DetailView):
    model = GeneralPackages
    template_name = "client/package_detail.html"
    context_object_name = "package"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["custom_packages"] = CustomPackages.objects.filter(
            package=self.object
        )

        return context


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


class ClientMessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "client/message_list.html"
    context_object_name = "messages_list"
    ordering = ["-id"]

    def get_queryset(self):
        return Message.objects.filter(
            client=self.request.user
        ).order_by("-id")


class ClientMessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "client/message_form.html"

    def form_valid(self, form):
        form.instance.client = self.request.user

        response = super().form_valid(form)

        messages.success(self.request, "Message sent successfully")

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Message was not sent successfully")

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("client_message_list")

class CustomLoginView(LoginView):

    template_name = 'login/login.html'

    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return reverse_lazy('home')
        else:
            return reverse_lazy('package_list')


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = RegisterForm()

    return render(request, 'login/register.html', {
        'form': form
    })

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Email is required.")
            return redirect('home')

        if NewsletterSubscriber.objects.filter(email=email).exists():
            messages.info(request, "You are already subscribed.")
            return redirect('home')

        NewsletterSubscriber.objects.create(email=email)

        messages.success(request, "Subscribed successfully!")
        return redirect('home')

    return redirect('home')

def send_newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            subscribers = NewsletterSubscriber.objects.values_list(
                "email", flat=True
            )

            for subscriber in subscribers:

                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="text-align:center;">
                        <h2>Get our offers </h2>
                    </div>

                    <h2>{subject}</h2>

                    <p>{message}</p>

                    <hr>

                    <p style="color:gray;font-size:12px;">
                       This is an automated email. Please do not reply to this message.
                    </p>
                </body>
                </html>
                """

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[subscriber],
                )

                email.attach_alternative(html_content, "text/html")
                email.send()

            return redirect("home")

    else:
        form = NewsletterForm()

    return render(request, "admin/newsletter.html", {"form": form})