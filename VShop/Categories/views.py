from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from Categories.models import Product, Category, UserProductRelation
from User.forms import UserRegistrationForm, UserAuthenticationForm


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        category = Category.objects.get(product_category=product)
        products = Category.objects.get(product_category=product).product_category.exclude(pk=pk)[:8]
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        extra_bar = "Products"
        context = {
            'product': product,
            'category': category,
            'products': products,
            'extra_bar': extra_bar,
            "reg_form": reg_form,
            "auth_form": auth_form,
        }
        return render(request, 'Categories/product_page.html', context)

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


class SearchResultsView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CategoriesProductsView(View):
    def get(self, request):
        categories = Category.objects.annotate(one=Count('product_category')).filter(one__gt=0)
        extra_bar = "Categories"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        context = {
            "categories": categories,
            "extra_bar": extra_bar,
            "reg_form": reg_form,
            "auth_form": auth_form,
        }
        return render(request, "Categories/categories_product_listing.html", context)

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


class CategoryProductsView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        products = Product.objects.filter(category=category)
        extra_bar = "Category Products"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        context = {
            "category": category,
            "products": products,
            "extra_bar": extra_bar,
            "reg_form": reg_form,
            "auth_form": auth_form,
        }
        return render(request, "Categories/category_product_listing.html", context)

    def post(self, request, pk):
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


# class UserProductRelation(View):
    # pass


def like_product(request, product_id, back_url):

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return redirect(back_url, product_id)
    user = request.user
    upr, created = UserProductRelation.objects.get_or_create(user=user, product=product)
    upr.like = not upr.like
    upr.save()
    return redirect(back_url, product_id)


