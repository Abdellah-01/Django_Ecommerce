from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'enquiry_name',
                'placeholder': 'Name *',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'enquiry_email',
                'placeholder': 'Email address *',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-control_gray',
                'placeholder': 'Your Message',
                'cols': 30,
                'rows': 8,
                'required': True
            }),
        }
