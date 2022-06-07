from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View

from Categories.models import Product, Category
from User.forms import UserRegistrationForm, UserAuthenticationForm
from country.models import Country
from promocode.models import PromoCode


class HomePageView(View):
    def get(self, request, name='Belarus'):
        res = "HELLO"
        user = request.user
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        cities = Country.objects.get(name=name).cities.values_list('id', flat=True)
        categories = Category.objects.filter(city__id__in=cities)
        promos_1 = PromoCode.objects.all()
        promos = promos_1[0:4]
        products_1 = Product.objects.filter(category__id__in=categories)
        products = products_1[0:8]
        extra_bar = "Home"
        context = {
            "res": res,
            "reg_form": reg_form,
            "auth_form": auth_form,
            "user": user,
            "categories": categories,
            "name": name,
            "products": products,
            "promos": promos,
            "promos_1": promos_1,
            "extra_bar": extra_bar,
        }
        return render(request, "mainpage/mainpage.html", context)

    def post(self, request):
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('user_page_my_account', user.email)
        else:
            print(reg_form.errors)
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('user_page_my_account', user.email)
        else:
            print(auth_form.errors)
        return render(request, "mainpage/mainpage.html", {"reg_form": reg_form, "auth_form": auth_form, "user": user})

