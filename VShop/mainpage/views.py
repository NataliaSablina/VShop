from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from Categories.models import Product, Category, UserProductRelation
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
        products_2 = UserProductRelation.objects.filter(user=user).order_by('like', 'view').values_list(
            'product',
            flat=True
        )
        products_ready = []
        if products_2.count() <= 3:
            products_ready.extend(products)
        else:
            products_ready = products[0:3]
        categories_2 = Product.objects.filter(id__in=products_ready).values_list('category', flat=True)
        recommended_products = Product.objects.filter(category__id__in=categories_2)
        relations = UserProductRelation.objects.filter(product__id__in=recommended_products).order_by('like', 'view')
        recommended_products_ready = list(Product.objects.filter(upr__id__in=relations)) + list(recommended_products)
        result_recommended = []
        for product in recommended_products_ready:
            if product not in result_recommended:
                result_recommended.append(product)
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
            "result_recommended":result_recommended,
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


class SearchProductsView(View):
    def get(self, request, name='Belarus'):
        word = request.GET.get('q')
        print(word)
        product_list = Product.objects.filter(Q(name__icontains=word) | Q(product_details__icontains=word))
        category_list = Category.objects.filter(Q(name__icontains=word))
        promo_code_list = PromoCode.objects.filter(Q(name__icontains=word) | Q(terms_conditions__icontains=word)
                                                   | Q(highlight__icontains=word))
        if len(product_list) < 1 and len(category_list) < 1 and len(promo_code_list) < 1:
            return redirect('search_not_done')
        else:
            context = {
                "product_list": product_list,
                "category_list": category_list,
                "promo_code_list": promo_code_list,
            }
            return render(request, "mainpage/search_done.html", context)


class SearchNotDoneView(View):
    def get(self, request, name='Belarus'):
        return render(request, "mainpage/search_not_done.html")
# object_list = City.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
