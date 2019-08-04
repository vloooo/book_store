from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# form for registration new user
class RegForm(forms.ModelForm):

    password_conf = forms.CharField(required=True,
                                    max_length=30,
                                    min_length=6,
                                    label='password again:',
                                    widget=forms.PasswordInput)

    password = forms.CharField(required=True,
                               max_length=30,
                               min_length=6,
                               widget=forms.PasswordInput)

    birthday = forms.DateField(input_formats=['%d/%m/%Y'])

    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_conf', 'gender', 'birthday')

    # validation matching passwords
    def clean_password_conf(self):
        pasw1 = self.cleaned_data['password_conf']
        pasw2 = self.cleaned_data['password']

        if pasw1 != pasw2:
            raise ValidationError('passwords didn\'t match')

        return pasw1
