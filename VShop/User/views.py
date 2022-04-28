from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import View
from .forms import UserRegistrationForm, UserAuthenticationForm
from django.shortcuts import redirect
from .models import User


def main_page(request):
    print(User.objects)
    res = "HELLO"
    print(request.user)
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            reg_form.save()
            return redirect('index2')
        else:
            print(reg_form.errors)
            print()
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index2')
        else:
            print(auth_form.errors)
    else:
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
    return render(request, "User/mainpage.html", {"res": res, "reg_form": reg_form, "auth_form": auth_form})


def index2(request):
    return render(request, "User/index.html")

# class UserRegistration(View):
#     def get(self, request):
#         form = UserRegistrationForm()
#         return render(request, "base.html", context={"form": form})
#
#     def post(self, request):
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid:
#             form.save()
#         return redirect('index')
#         # return redirect(request, "index.html", context={"form":form})
