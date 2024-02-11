from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import CreateUserForm
from django.http import HttpRequest


def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(request.GET.get("next", "/shop"))

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            # login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect(request.GET.get("next", 'shop/'))
    else:
        form = CreateUserForm()

    context = {"form": form, "next": request.GET.get("next", 'shop/')}
    return render(request, "registration/register.html", context=context)


def base(request: HttpRequest):
    return redirect('shop/')
