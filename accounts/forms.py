from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import VulnTrackAccounts


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = VulnTrackAccounts
        fields = ('username', 'email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
