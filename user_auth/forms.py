from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegForm(forms.ModelForm):
    password_conf = forms.CharField(required=True, max_length=30, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'extradata.birthday', 'extradata.gemder')

    def clean_password_conf(self):
        pasw1 = self.cleaned_data['passwordconf']
        pasw2 = self.cleaned_data['password']
        if pasw1 != pasw2:
            raise ValidationError('not_allowed_val')
        return pasw1
