from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

from Categories.models import Product, Category, UserProductRelation, CommentProduct, UserCommentRelation
from User.forms import UserRegistrationForm, UserAuthenticationForm


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            user = request.user
            upr, created = UserProductRelation.objects.get_or_create(user=user, product=product)
            upr.view = True
            upr.save()
            # try:
            #     product = Product.objects.get(pk=product_id)
            # except Product.DoesNotExist:
            #     return redirect(back_url, product_id)
            # user = request.user
            # upr, created = UserProductRelation.objects.get_or_create(user=user, product=product)
            # upr.like = not upr.like
            # upr.save()

        # product.review = product.review + 1
        # product.save()
        category = Category.objects.get(product_category=product)
        products = Category.objects.get(product_category=product).product_category.exclude(pk=pk)[:8]
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        # blog_object.blog_views = blog_object.blog_views + 1
        # blog_object.save()
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

    def get_object(self):
        obj = super().get_object()
        obj.review += 1
        obj.save()
        return obj


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


class RecommendedProductsView(View):
    def get(self, request):
        user = request.user
        products = UserProductRelation.objects.filter(user=user).order_by('like', 'view').values_list(
            'product',
            flat=True
        )
        products_ready = []
        if products.count() <= 3:
            products_ready.extend(products)
        else:
            products_ready = products[0:3]
        categories = Product.objects.filter(id__in=products_ready).values_list('category', flat=True)
        recommended_products = Product.objects.filter(category__id__in=categories)
        relations = UserProductRelation.objects.filter(product__id__in=recommended_products).order_by('like', 'view')
        recommended_products_ready = list(Product.objects.filter(upr__id__in=relations)) + list(recommended_products)
        result_recommended = []
        for product in recommended_products_ready:
            if product not in result_recommended:
                result_recommended.append(product)
        return render(request, "Categories/none.html")


class CommentsView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        comments = product.comment.all()
        context = {
            "comments": comments,
            "product": product,

        }
        return render(request, "Categories/product_comment.html", context)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        data = request.POST
        if data.get('comment_id'):
            parent_comment = CommentProduct.objects.get(pk=data.get('comment_id'))
        else:
            parent_comment = None
        comment = CommentProduct(
            user=request.user,
            product=product,
            comment=parent_comment,
            content=data['content_comment']
        )
        comment.save()
        print(data)
        return redirect('comments', pk)


class CommentLikeView(View):
    def get(self, request, pk, product_id, back_url):
        user = request.user
        try:
            comment = CommentProduct.objects.get(pk=pk)
        except CommentProduct.DoesNotExist:
            return redirect(back_url, product_id)
        comment_like, created = UserCommentRelation.objects.get_or_create(user=user, comment=comment)
        comment_like.like = not comment_like.like
        comment_like.save()
        return redirect(back_url, product_id)
