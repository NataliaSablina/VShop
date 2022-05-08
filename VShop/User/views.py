from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.generic import View
from .forms import UserRegistrationForm, UserAuthenticationForm
from django.shortcuts import redirect
from .models import User


class HomePage(View):
    def get(self, request):
        res = "HELLO"
        print(request.user)
        user = request.user
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/mainpage.html", {"res": res, "reg_form": reg_form, "auth_form": auth_form, "user": user})

    def post(self, request):
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('user_page', user.email)
        else:
            print(reg_form.errors)
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user.is_active:
                login(request, user)
                return redirect('user_page', user.email)
        else:
            print(auth_form.errors)
        return render(request, "User/mainpage.html", {"reg_form": reg_form, "auth_form": auth_form, "user": user})


class UserPage(View):
    def get(self, request, email):
        print(email)
        user = User.objects.get(email=email)
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, 'User/user_page.html', {"user":  user, "reg_form": reg_form, "auth_form": auth_form})

    def post(self, request, email):
        pass
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('user_page', user.email)
        else:
            print(reg_form.errors)
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user.is_active:
                login(request, user)
                return redirect('user_page', user.email)
        else:
            print(auth_form.errors)
        return render(request, "User/user_page.html", {"reg_form": reg_form, "auth_form": auth_form, "user": user})


class UserAdminView(View):
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()


def index2(request):
    return render(request, "User/index.html")


def logout_view(request):
    logout(request)
    return redirect('home_page')


