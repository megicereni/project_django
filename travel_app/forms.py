from django.forms import forms
from travel_app.models import GeneralPackages, CustomPackages, Attraction, PackagesAttraction, Booking


class GeneralPackageForm(forms.ModelForm):
    class Meta:
        model = GeneralPackages
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control',
            'placeholder':'Enter Package Title',}),
            'description': forms.Textarea(attrs={'class':'form-control',
            'rows': 3,
            'placeholder':'Enter Package Description',
            }),
            'price': forms.TextInput(attrs={'class':'form-control',}),
            'destination': forms.TextInput(attrs={'class':'form-control',}),
            'days': forms.TextInput(attrs={'class': 'form-control', }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
    def clean_price(self):
        if self.cleaned_data['price']<0:
           raise forms.ValidationError("Price cannot be less than 0")
        return self.cleaned_data['price']

class CustomPackageForm(forms.ModelForm):
    class Meta:
        model = CustomPackages
        fields = '__all__'
        widgets = {
            'departureDate':forms.DateInput(
                attrs={
                    'type':'date',
                    'class':'form-control'
                }
            ),
            'arrivalDate': forms.DateInput(
                attrs={
                    'type':'date',
                    'class':'form-control'
                }),
            'limitNumberOfPeople':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Number of People in Tour'
                }),
            'price':forms.TextInput(
                attrs={
                    'class':'form-control',
                }),
        }
    def clean_price(self):
        if self.cleaned_data['price']<0:
            raise forms.ValidationError('Price cannot be less than 0')
        return self.cleaned_data['price']
    def clean_arrivalDate(self):
        arrivalDate=self.cleaned_data['arrivalDate']
        departureDate=self.cleaned_data['departureDate']

        if arrivalDate<departureDate:
            raise forms.ValidationError('Arrival date cannot be before than departure date')
        return arrivalDate

class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields=['name','location']
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'location':forms.TextInput(
                attrs={
                    'class':'form-control',
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
