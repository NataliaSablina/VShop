from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin

from Categories.models import Category, Product
from User.forms import UserRegistrationForm, UserAuthenticationForm
from promocode.models import PromoCode


class AvailablePromosView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        categories_id_list = Product.objects.filter(promo_code__isnull=False).values_list('category', flat=True)
        categories = Category.objects.filter(id__in=categories_id_list)[:3]
        extra_bar = "Promos"
        context = {
            "categories": categories,
            "extra_bar": extra_bar,
        }
        return render(request, 'promocode/promos.html', context)

    def post(self, request):
        pass


class PromoListView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        product = Product.objects.filter(category=category, promo_code__isnull=False)
        promos = PromoCode.objects.filter(product_promo__id__in=product)
        products = product.all()
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        extra_bar = "Promos"
        print(promos)
        print(products)
        context = {
            "promos": promos,
            "products": products,
            "extra_bar": extra_bar,
            "reg_form": reg_form,
            "auth_form":auth_form,
        }
        return render(request, "promocode/promos_category_page.html", context)

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


class PromoPageView(View):
    def get(self, request, pk_1, pk_2):
        promo_code = PromoCode.objects.get(pk=pk_1)
        product = Product.objects.get(pk=pk_2)
        extra_bar = "Promos"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        context = {
            "promo_code": promo_code,
            "product": product,
            "extra_bar": extra_bar,
            "reg_form": reg_form,
            "auth_form": auth_form,
        }
        return render(request, "promocode/promo_page.html", context)

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


class AllAvailablePromosCategoriesView(View):
    def get(self, request):
        categories_id_list = Product.objects.filter(promo_code__isnull=False).values_list('category', flat=True)
        categories = Category.objects.filter(id__in=categories_id_list)
        extra_bar = "Promos"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        context = {
            "categories": categories,
            "extra_bar": extra_bar,
            "reg_form":reg_form,
            "auth_form": auth_form,
        }
        return render(request, 'promocode/all_promo_categories.html', context)

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




