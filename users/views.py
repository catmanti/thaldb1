from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, "Logged in successfully!")
            return redirect("users:index")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def test_view(request):
    return render(request, "test.html")
