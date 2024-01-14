from django.shortcuts import render, redirect

from .forms import CreateUserForm
from django.http import HttpResponse, HttpRequest


def register(request: HttpRequest):
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next", 'article:article'))
    else:
        form = CreateUserForm()

    context = {"form": form}
    return render(request, "registration/register.html", context=context)
