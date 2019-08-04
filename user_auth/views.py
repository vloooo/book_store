from django.shortcuts import render
from user_auth.forms import RegForm
from user_auth.models import ExtraData
from datetime import datetime


def register(request):
    """
    view for registration new user
    """
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

            return render(request, 'user_auth/scs.html')

        else:
            context = {'form': form}
            return render(request, 'user_auth/register.html', context)

    else:
        form = RegForm()
        context = {'form': form}
        return render(request, 'user_auth/register.html', context)
