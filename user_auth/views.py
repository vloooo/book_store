from django.shortcuts import render
from django.contrib.auth.models import User
from user_auth.forms import RegForm


def register(request):
    if request.method == request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user_auth/scs.html')
        else:
            context = {'form': form}
            return render(request, 'user_auth/register.html', context)

    else:
        form = RegForm()
        context = {'form': form}
        return render(request, 'user_auth/register.html', context)


