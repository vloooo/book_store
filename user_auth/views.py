from django.shortcuts import render, redirect
from user_auth.forms import RegForm, AuthForm, EditProfileForm
from user_auth.models import ExtraData
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def registration(request):

    if request.method == 'POST':
        form = RegForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()

            # additional data for standard user model
            ExtraData.objects.create(user=user,
                                     gender=request.POST['gender'],
                                     birthday=datetime.strptime(request.POST['birthday'], '%d/%m/%Y'))

            authenticate(request, username=user.username, password=request.POST['password'])
            login(request, user)
            return render(request, 'user_auth/scs.html')

        else:
            context = {'form': form}
            return render(request, 'user_auth/register.html', context)

    else:
        form = RegForm()
        context = {'form': form}
        return render(request, 'user_auth/register.html', context)


def login_view(request):

    if request.method == 'POST':
        form = AuthForm(data=request.POST)

        if form.is_valid():
            login(request, form.user_cache)
            return render(request, 'user_auth/scs.html')

        else:
            context = {'form': form}
            return render(request, 'user_auth/register.html', context)

    else:
        form = AuthForm()
        context = {'form': form}
        return render(request, 'user_auth/register.html', context)


def profile_view(request):
    context = {}
    return render(request, 'user_auth/profile.html', context)


def profile_edit_view(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()
            # fill birthday and gender fields that store in another model with OneToOne relationship to User
            ExtraData.objects.filter(user=user).update(gender=form.cleaned_data.get('gender'),
                                                       birthday=form.cleaned_data.get('birthday'))
            return redirect('auth:profile')

        else:
            context = {'form': form}
            return render(request, 'user_auth/register.html', context)

    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'user_auth/register.html', context)
