from django.forms import forms
from travel_app.models import GeneralPackages, CustomPackages, Attraction, PackagesAttraction, Booking, Message, Review


class GeneralPackageForm(forms.ModelForm):
    class Meta:
        model = GeneralPackages
        fields = '__all__'
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
        fields = '__all__'
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


class PackageAttractionForm(forms.ModelForm):
    class Meta:
        model = PackagesAttraction
        fields = ['attraction', 'day_number']

        widgets = {
            'day_number': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'attraction': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'body': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'rows': 5
            })
        }
        labels = {
            'body': 'Message'
        }


class ReviewForm(forms.ModelForm):
    # Fusha ekstra — vijnë nga user-i i loguar, nuk ruhen në model
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'readonly': 'readonly',
            'placeholder': 'Email'
        })
    )

    organization = forms.ChoiceField(choices=[
        ('', 'Organization'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ])
    staff = forms.ChoiceField(choices=[
        ('', 'Staff'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ])
    price = forms.ChoiceField(choices=[
        ('', 'Price'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ])

    class Meta:
        model = Review
        fields = ['comment', 'organization', 'staff', 'price']  # ✅ vetëm fushat e modelit
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Your review...',
                'rows': 5
            })
        }
