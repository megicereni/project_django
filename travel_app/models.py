from django.db import models
from django.contrib.auth.models import AbstractUser


class GeneralPackages(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    destination = models.CharField(max_length=100)
    days = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='packages_images/', null=True, blank=True)
    attractions = models.ManyToManyField(
        'Attraction',
        through='PackagesAttraction',
        related_name='packages'
    )


class CustomPackages(models.Model):
    departureDate = models.DateField()
    arrivalDate = models.DateField()
    limitNumberOfPeople = models.IntegerField()
    price = models.IntegerField(default=0)
    package = models.ForeignKey(GeneralPackages, on_delete=models.CASCADE)


class Attraction(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class PackagesAttraction(models.Model):
    day = models.PositiveIntegerField()
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    package = models.ForeignKey(GeneralPackages, on_delete=models.CASCADE)


class Client(AbstractUser):
    phone = models.CharField(max_length=20)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Confirmed'),
        ('rejected', 'Cancelled'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    package = models.ForeignKey(CustomPackages, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    numberOfPeople = models.IntegerField(default=1)
    totalPrice = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')

    def __str__(self):
        return self.package.package.title


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    responseMessage = models.TextField(blank=True)


class Review(models.Model):
    REVIEW_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    content = models.TextField()
    organization = models.CharField(choices=REVIEW_CHOICES, max_length=20)
    staff = models.CharField(choices=REVIEW_CHOICES, max_length=20)
    price = models.CharField(choices=REVIEW_CHOICES, max_length=20)


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    refundedAmount = models.IntegerField()

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email