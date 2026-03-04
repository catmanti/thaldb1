from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


def login_view(request):
    return redirect("login")


def test_view(request):
    return render(request, "test.html")
