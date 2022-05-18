from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from Categories.models import Category, Product
from VShop import settings
from country.models import Country
from promocode.models import PromoCode
from .forms import UserRegistrationForm, UserAuthenticationForm, ChangeUserInformation, ChangeUserPassword, ContactForm,\
    DeactivateAccount
from django.shortcuts import redirect
from .models import User
from django.core import mail


class HomePage(View):
    def get(self, request, name='Belarus'):
        res = "HELLO"
        print(request.user)
        user = request.user
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        cities = Country.objects.get(name=name).cities.values_list('id', flat=True)
        categories = Category.objects.filter(city__id__in=cities)
        print(categories)
        promos_1 = PromoCode.objects.filter(category__id__in=categories)
        promos = promos_1[0:4]
        products_1 = Product.objects.filter(category__id__in=categories)
        products = products_1[0:8]
        context = {
            "res": res,
            "reg_form": reg_form,
            "auth_form": auth_form,
            "user": user,
            "categories": categories,
            "name": name,
            "products": products,
            "promos": promos,
        }
        return render(request, "User/mainpage.html", context)

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
        return render(request, "User/mainpage.html", {"reg_form": reg_form, "auth_form": auth_form, "user": user})


class UserPage(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request, email):
        print(email)
        user = User.objects.get(email=email)
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        user_change_form = ChangeUserInformation(instance=request.user)
        return render(request, 'User/user_page_my_account.html', {"user": user, "reg_form": reg_form,
                                                                  "auth_form": auth_form,
                                                                  "user_change_form": user_change_form,
                                                                  })

    def post(self, request, email):
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        user_change_form = ChangeUserInformation(data=request.POST, instance=request.user)

        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('user_page_my_account', user.email)
        else:
            print(reg_form.errors)
        if user_change_form.is_valid():
            user = user_change_form.save()
            return redirect('user_page_my_account', user.email)
        else:
            print(user_change_form.errors)
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('user_page_my_account', user.email)
        else:
            print(auth_form.errors)

        return render(request, "User/user_page_my_account.html", {"reg_form": reg_form,
                                                                  "auth_form": auth_form,
                                                                  "user_change_form": user_change_form,

                                                                  })


class ChangePassword(View):
    def get(self, request, email):
        user = User.objects.get(email=email)
        change_password_form = ChangeUserPassword()
        return render(request, 'User/user_page_change_password.html', {"user": user,
                                                                       "change_password_form": change_password_form,
                                                                       })

    def post(self, request, email):
        change_password_form = ChangeUserPassword(request.POST)
        if change_password_form.is_valid():
            # data = change_password_form.cleaned_data
            user = request.user
            print(change_password_form.cleaned_data['old_password'])
            if check_password(change_password_form.cleaned_data['old_password'], request.user.password):
                user.set_password(change_password_form.cleaned_data['new_password'])
                user.save()
                return redirect('home_page')
            else:
                raise ValueError('ffffffffffffffff')
        else:
            print(change_password_form.errors)
            return render(request, "User/user_page_change_password.html",
                          {"change_password_form": change_password_form})


class DeactivateAccountView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        user_deactivate_form = DeactivateAccount()
        return render(request, "User/deactivate.html", {"user_deactivate_form": user_deactivate_form})

    def post(self, request):
        user_deactivate_form = DeactivateAccount(request.POST)
        if user_deactivate_form.is_valid():
            if check_password(user_deactivate_form.cleaned_data['password'], request.user.password):
                user = request.user
                user.is_active = False
                user.save()
                logout(request)
                return redirect('home_page')
            else:
                print('fffffffffffffff')
        else:
            print(user_deactivate_form.errors)
        return redirect('index')


class DeleteAccount(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        return render(request, "User/delete_account.html")

    def post(self, request):
        user = request.user
        user.delete()
        logout(request)
        return redirect('home_page')


class ForgotPassword(View):
    def get(self, request):
        return render(request, "User/forgot_password.html")

    def post(self, request):
        pass


#
# class UserAdminView(View):
#     def get(self, request):
#         if request.user.is_superuser:
#             users = User.objects.all()


def index2(request):
    return render(request, "User/index.html")


def logout_view(request):
    logout(request)
    return redirect('home_page')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=mail)  # email в форме регистрации проверен на уникальность
            subject = 'Запрошен сброс пароля'
            email_template_name = "User/forgot_password.html"
            cont = {
                "email": user.email,
                'domain': '127.0.0.1:8000',  # доменное имя сайта
                'site_name': 'Website',  # название своего сайта
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
                "user": user,  # чтобы обратиться в письме по логину пользователя
                'token': default_token_generator.make_token(user),  # генерируем токен
                'protocol': 'http',
            }
            msg_html = render_to_string(email_template_name, cont)
            try:
                send_mail(subject, 'ссылка', 'admin@django-project.site', [user.email], fail_silently=True,
                          html_message=msg_html)
            except BadHeaderError:
                return HttpResponse('Обнаружен недопустимый заголовок!')
            return redirect("password_reset_done")
    else:
        password_reset_form = PasswordResetForm()
    return render(request=request, template_name="User/forgot_password.html",
                  context={"password_reset_form": password_reset_form})


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            to_email = ['nataliasablina0@gmail.com']
            print(to_email)
            try:
                # with mail.get_connection() as connection:
                #     mail.EmailMessage(subject, message, from_email, to_email,
                #                       connection=connection).send()
                send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=to_email)
                sent = True
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "User/contact.html", {'form': form})


def success(request):
    return render(request, "User/success.html")


class TermsConditionsView(View):
    def get(self, request):
        return render(request, 'User/terms_conditions.html')

    def post(self, request):
        pass


class HelpSupportView(View):
    def get(self, request):
        return render(request, 'User/help_support.html')

    def post(self, request):
        pass


class TicketView(View):
    def get(self, request):
        return render(request, 'User/tickets.html')

    def post(self, request):
        pass


class AddressView(View):
    def get(self, request):
        return render(request, 'User/adress.html')

    def post(self, request):
        pass


class AvailablePromosView(View):
    def get(self, request):
        return render(request, 'User/promos.html')

    def post(self, request):
        pass


# def send_email(request):
#     msg = EmailMessage('Request Callback',
#                        'Here is the message.', to=['natalasablina78@gmail.com'])
#     msg.send()
#     return HttpResponseRedirect('/')
