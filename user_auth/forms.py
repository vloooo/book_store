from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user_auth.models import Gender


class RegForm(forms.ModelForm):
    password_conf = forms.CharField(required=True, max_length=30, min_length=6)
    birthday = forms.DateField()
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_conf', 'gender', 'birthday')

    def clean_password_conf(self):
        pasw1 = self.cleaned_data['passwordconf']
        pasw2 = self.cleaned_data['password']
        if pasw1 != pasw2:
            raise ValidationError('not_allowed_val')
        return pasw1
