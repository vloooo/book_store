from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


# form for registration new user
class RegForm(forms.ModelForm, ):

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
            raise forms.ValidationError('passwords didn\'t match')

    # validation for uniq. email
    def clean_email(self):
        users = User.objects.filter(email=self.cleaned_data['email'])
        if users.exists():
            raise forms.ValidationError('This email is used for another account. Please, enter another one.')


class AuthForm(AuthenticationForm):
    username = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    field_order = ['username', 'email', 'password']

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # if username field was empty, get it by email
    def get_username(self):
        if self.cleaned_data.get('username') != '':
            return self.cleaned_data.get('username')
        else:
            return User.objects.get(email=self.cleaned_data.get('email')).username

    # standard AuthenticationForm validation with new way obtaining username
    def clean(self):

        username = self.get_username()
        password = self.cleaned_data.get('password')

        # check if exist user that have this credentials
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
