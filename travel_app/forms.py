from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from travel_app.models import GeneralPackages, CustomPackages, Attraction, PackagesAttraction, Booking, Message, Review, \
    Client


class GeneralPackageForm(forms.ModelForm):
    class Meta:
        model = GeneralPackages
        fields = ['title', 'description', 'price', 'destination', 'days', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter Package Title', }),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3,
                                                 'placeholder': 'Enter Package Description',
                                                 }),
            'price': forms.TextInput(attrs={'class': 'form-control', }),
            'destination': forms.TextInput(attrs={'class': 'form-control', }),
            'days': forms.TextInput(attrs={'class': 'form-control', }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_price(self):
        if self.cleaned_data['price'] < 0:
            raise forms.ValidationError("Price cannot be less than 0")
        return self.cleaned_data['price']


class CustomPackageForm(forms.ModelForm):
    class Meta:
        model = CustomPackages
        exclude = ['package', 'arrivalDate']
        widgets = {
            'departureDate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'limitNumberOfPeople': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Number of People in Tour'
                }),
            'price': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
        }

    def clean_price(self):
        if self.cleaned_data['price'] < 0:
            raise forms.ValidationError('Price cannot be less than 0')
        return self.cleaned_data['price']


class ResponseMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['responseMessage']
        widgets = {
            'responseMessage': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            })
        }


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['numberOfPeople']
        widgets = {
            'numberOfPeople': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter number of people',
                'min': 1,
            })
        }
        labels = {
            'numberOfPeople': 'Number of People'
        }

    def clean_numberOfPeople(self):
        numberOfPeople = self.cleaned_data['numberOfPeople']
        if numberOfPeople < 1:
            raise forms.ValidationError('Number of people must be at least 1.')
        return numberOfPeople


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['booking', 'content', 'organization', 'staff', 'price']

        widgets = {
            'booking': forms.Select(attrs={
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...',
            }),
            'organization': forms.Select(attrs={
                'class': 'form-control',
            }),
            'staff': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def clean_content(self):
        content = self.cleaned_data['content']

        if len(content) < 10:
            raise forms.ValidationError(
                "Review must contain at least 10 characters"
            )

        return content


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message...'
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+355 69 xxx xxxx'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:

        model = Client

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'username',
            'password1',
            'password2'
        ]


class NewsletterForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Subject",
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Message",
            "rows": 6,
        })
    )
