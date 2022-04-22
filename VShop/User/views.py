from django.shortcuts import render


def index(request):
    res = "HELLO"
    return render(request, "User/mainpage.html", {"res":res})
