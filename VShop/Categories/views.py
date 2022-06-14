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

        gt = request.POST.get('r1')
        print(gt)
        print(request.POST.get('r2'))
        print(request.POST.get('sum'))
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
    # def post(self, request, pk):
    #     product = Product.objects.get(pk=pk)
    #     data = request.POST
    #     if data.get('comment_id'):
    #         parent_comment = CommentProduct.objects.get(pk=data.get('comment_id'))
    #     else:
    #         parent_comment = None
    #     comment = CommentProduct(
    #         user=request.user,
    #         product=product,
    #         comment=parent_comment,
    #         content=data['content_comment']
    #     )
    #     comment.save()
    #     print(data)
    #     return redirect('comments', pk)


class CategoryProductsView(View):
    def get(self, request, pk):
        gt = request.GET.get('r1')
        print(gt)
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
        gt = request.GET.get('r1')
        print(gt)
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
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        user = request.user
        products = UserProductRelation.objects.filter(user=user).order_by('like', 'view').values_list(
            'product',
            flat=True
        )
        print(products)
        products_ready = products[0:3]
        # if products.count() <= 3:
        #     products_ready.extend(products)
        # else:
        #     products_ready = products[0:3]
        print(products_ready)
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


class CreateBookMarkView(View):

    def get(self, request, product_id, back_url):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return redirect(back_url, product_id)

        product_bookmark, created = UserProductRelation.objects.get_or_create(user=request.user, product=product)
        product_bookmark.in_bookmarks = not product_bookmark.in_bookmarks
        product_bookmark.save()
        return redirect(back_url, product_id)


class UserBookmarksListView(View):

    def get(self, request):
        user = request.user
        products_id_list = UserProductRelation.objects.filter(user=user, in_bookmarks=True).values_list(
            'product',
            flat=True
        )
        products = Product.objects.filter(id__in=products_id_list)
        context = {
            "products": products,
        }
        return render(request, "Categories/none.html", context)


class SortFilterPageView(View):
    sort_dict = {
        'TOP_RATE': 1,
        'HIGH_TO_LOW': 2,
        'LOW_TO_HIGH': 3,
        'MOST_POPULAR': 4,
    }

    def get(self, request, sorting_id, filter_str=None):
        if not (4 < sorting_id < 0):
            sorting_id = 1
        extra_bar = 'Listing'
        context = {
            'extra_bar': extra_bar,
        }
        if filter_str is None:
            fd = {}
        else:
            filter_list_start = filter_str.split('&')
            fd = {}
            for element in filter_list_start:
                fd[element] = True
                if 'isnull' in element:
                    fd[element] = False
        if sorting_id == self.sort_dict['TOP_RATE']:
            products = sorted(Product.objects.filter(**fd), key=lambda p: p.rating, reverse=True)
            context['products'] = products
        if sorting_id == self.sort_dict['HIGH_TO_LOW']:
            products = Product.objects.filter(**fd).order_by('-price')
            context['products'] = products
        if sorting_id == self.sort_dict['LOW_TO_HIGH']:
            products = Product.objects.filter(**fd).order_by('price')
            context['products'] = products
        if sorting_id == self.sort_dict['MOST_POPULAR']:
            products = sorted(Product.objects.filter(**fd), key=lambda p: p.popular, reverse=True)
            context['products'] = products
        return render(request, 'Categories/sort_filter_page.html', context)


class SortProducts(View):
    sort_dict = {
        'TOP_RATE': 1,
        'HIGH_TO_LOW': 2,
        'LOW_TO_HIGH': 3,
        'MOST_POPULAR': 4,
    }

    def get(self, request, back_url):
        return redirect(back_url, 1)

    def post(self, request, back_url):
        filter_dict = ''
        if request.POST.get('r2') and request.POST.get('r3'):
            filter_dict += 'delivery__free' + '&' + 'promo_code__isnull'
        elif request.POST.get('r2'):
            filter_dict += 'delivery__free'
        elif request.POST.get('r3'):
            filter_dict += 'promo_code__isnull'
        if filter_dict:
            return redirect(back_url, self.sort_dict.get(request.POST.get('sum', 1)), filter_dict)
        return redirect(back_url, self.sort_dict.get(request.POST.get('sum', 1), 1))

        # if int(request.POST.get('sum')) == self.sort_dict['TOP_RATE']:
        #     return redirect(back_url, self.sort_dict['TOP_RATE'], filter_dict)
        # if int(request.POST.get('sum')) == self.sort_dict['HIGH_TO_LOW']:
        #     return redirect(back_url, 2, filter_dict)
        # if int(request.POST.get('sum')) == self.sort_dict['LOW_TO_HIGH']:
        #     return redirect(back_url, 3, filter_dict)
        # if int(request.POST.get('sum')) == self.sort_dict['MOST_POPULAR']:
        #     return redirect(back_url, 4, filter_dict)






      # if sorting_id == self.sort_dict['TOP_RATE']:
      #           products = sorted(Product.objects.all(), key=lambda p: p.rating, reverse=True)
      #           context['products'] = products
      #       if sorting_id == self.sort_dict['HIGH_TO_LOW']:
      #           products = sorted(Product.objects.all(), key=lambda p: p.price, reverse=True)
      #           context['products'] = products
      #       if sorting_id == self.sort_dict['LOW_TO_HIGH']:
      #           products = sorted(Product.objects.all(), key=lambda p: p.price)
      #           context['products'] = products
      #       if sorting_id == self.sort_dict['MOST_POPULAR']:
      #           products = sorted(Product.objects.all(), key=lambda p: p.popular, reverse=True)
      #           context['products'] = products