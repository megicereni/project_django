from django import forms
from travel_app.models import GeneralPackages, CustomPackages, Attraction, PackagesAttraction, Booking, Message, Review


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
        exclude=['package']
        widgets = {
            'departureDate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'arrivalDate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }),
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

    def clean_arrivalDate(self):
        arrivalDate = self.cleaned_data['arrivalDate']
        departureDate = self.cleaned_data['departureDate']

        if arrivalDate < departureDate:
            raise forms.ValidationError('Arrival date cannot be before than departure date')
        return arrivalDate

class ResponseMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['responseMessage']
        widgets ={
            'responseMessage': forms.TextInput(attrs={
                'class': 'form-control',
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

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['name', 'email', 'body']
#         widgets = {
#             'name': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
#             'body': forms.Textarea(attrs={
#                 'placeholder': 'Write your message here...',
#                 'rows': 5
#             })
#         }
#         labels = {
#             'body': 'Message'
#         }

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        exclude = ['user']

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),

            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your review',
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

    def clean_review(self):

        if len(self.cleaned_data['review']) < 10:

            raise forms.ValidationError(
                "Review must contain at least 10 characters")

        return self.cleaned_data['review']