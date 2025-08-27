from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control_gray",
                "placeholder": "Password *",
                "id": "customerPasswordRegisterInput"
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control_gray",
                "placeholder": "Re-Enter Password *",
                "id": "customerConfirmPasswordRegisterInput"  # ✅ updated
            }
        )
    )


    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "password"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control form-control_gray",
                "placeholder": "First Name",
                "id": "customerFirstNameRegisterInput"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control form-control_gray",
                "placeholder": "Last Name",
                "id": "customerLastNameRegisterInput"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control form-control_gray",
                "placeholder": "Email Address *",
                "id": "customerEmailRegisterInput"
            }),
            "mobile_number": forms.TextInput(attrs={
                "class": "form-control form-control_gray",
                "placeholder": "Mobile Number",
                "id": "customerMobileRegisterInput",
                 "required": True,
            }),
        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does Not Match!"
            )

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class']
