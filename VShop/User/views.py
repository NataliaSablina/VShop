from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
from VShop import settings
from promocode.models import PromoCode
from .forms import UserRegistrationForm, UserAuthenticationForm, ChangeUserInformation, ChangeUserPassword, ContactForm, \
    DeactivateAccount, ActivateAccountForm, HelpClientForm
from .models import User


class UserPageView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request, email):
        user = User.objects.get(email=email)
        extra_bar = "My Account"
        user_change_form = ChangeUserInformation(instance=request.user)
        context = {
            "user": user,
            "user_change_form": user_change_form,
            "extra_bar": extra_bar,
        }
        return render(request, 'User/user_page_my_account.html', context)

    def post(self, request, email):
        user_change_form = ChangeUserInformation(data=request.POST, instance=request.user)
        if user_change_form.is_valid():
            user = user_change_form.save()
            return redirect('user_page_my_account', user.email)
        else:
            print(user_change_form.errors)
        context = {
            "user_change_form": user_change_form,
        }
        return render(request, "User/user_page_my_account.html",  context)


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request, email):
        user = User.objects.get(email=email)
        change_password_form = ChangeUserPassword()
        extra_bar = "Change Password"
        context = {
            "user": user,
            "change_password_form": change_password_form,
            "extra_bar": extra_bar,
        }
        return render(request, 'User/user_page_change_password.html', context)

    def post(self, request, email):
        change_password_form = ChangeUserPassword(request.POST)
        if change_password_form.is_valid():
            user = request.user
            if check_password(change_password_form.cleaned_data['old_password'], request.user.password):
                user.set_password(change_password_form.cleaned_data['new_password'])
                user.save()
                return redirect('home_page')
            else:
                raise ValueError('ffffffffffffffff')
        else:
            print(change_password_form.errors)
            context = {
                "change_password_form": change_password_form,
            }
            return render(request, "User/user_page_change_password.html", context)


class DeactivateAccountView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        user_deactivate_form = DeactivateAccount()
        extra_bar = "Activate Account"
        context = {
            "user_deactivate_form": user_deactivate_form,
            "extra_bar": extra_bar
        }
        return render(request, "User/deactivate.html", context)

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
        return redirect('deactivate')


class DeleteAccountView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Delete Account"
        return render(request, "User/delete_account.html", {"extra_bar": extra_bar})

    def post(self, request):
        user = request.user
        user.delete()
        logout(request)
        return redirect('home_page')


class ForgotPasswordView(View):
    def get(self, request):
        extra_bar = "Forgot Password"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/forgot_password.html",
                      {"extra_bar": extra_bar, "reg_form": reg_form, "auth_form": auth_form})

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


@login_required(login_url='home_page')
def logout_view(request):
    logout(request)
    return redirect('home_page')


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
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
        if form.is_valid():
            subject = "Reset password link"
            message = "Reset password link:"
            to_email = form.cleaned_data['to_email']
            email_template_name = "User/test.html"
            user = User.objects.get(email=to_email)
            cont = {
                "email": user.email,
                'domain': '127.0.0.1:8000',  # ???????????????? ?????? ??????????
                'site_name': 'VShop',  # ???????????????? ???????????? ??????????
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # ?????????????? ??????????????????????????
                "user": to_email,  # ?????????? ???????????????????? ?? ???????????? ???? ???????????? ????????????????????????
                'token': default_token_generator.make_token(user),  # ???????????????????? ??????????
                'protocol': 'http',
            }
            ref = cont.get('protocol') + '://' + cont.get('domain') + '/user/' + 'password_reset_confirm/' + str(
                cont.get('uid')) + '/' + str(cont.get('token'))
            msg_html = render_to_string(email_template_name, {"ref": ref})
            try:
                send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email],
                          fail_silently=True, html_message=msg_html)
                sent = True
            except BadHeaderError:
                return HttpResponse('???????????? ?? ???????? ????????????.')
            return redirect('send_mail_success')
        else:
            return HttpResponse('???????????????? ????????????.')
    extra_bar = "Reset Password"
    return render(request, "User/reset_password_email.html", {'form': form, "extra_bar": extra_bar})


class SendMailSuccess(View):
    def get(self, request):
        return render(request, "User/send_mail_success.html")


class TermsConditionsView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Terms & Conditions"
        return render(request, 'User/terms_conditions.html', {"extra_bar": extra_bar})

    def post(self, request):
        pass


class HelpSupportView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Help & Support"
        return render(request, 'User/help_support.html', {"extra_bar": extra_bar})

    def post(self, request):
        pass


class AddressView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "My Address"
        return render(request, 'User/adress.html', {"extra_bar": extra_bar})

    def post(self, request):
        pass


class ActivateAccountView(View):
    def get(self, request):
        activate_account_form = ActivateAccountForm()
        extra_bar = "Activate Account"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/activate_deactivated_account.html",
                      {"activate_account_form": activate_account_form, "extra_bar": extra_bar, "reg_form": reg_form,
                       "auth_form": auth_form})

    def post(self, request):
        activate_account_form = ActivateAccountForm(request.POST)
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
        if activate_account_form.is_valid():
            email = activate_account_form.cleaned_data["email"]
            subject = activate_account_form.cleaned_data["subject"]
            message_commit = activate_account_form.cleaned_data["message"]
            message = message_commit + email
            try:
                send_mail(subject, message=message, from_email=email, recipient_list=[settings.EMAIL_HOST_USER],
                          fail_silently=True)
                sent = True
            except BadHeaderError:
                return HttpResponse('???????????? ?? ???????? ????????????.')
            return redirect('success')
        return render(request, "User/activate_deactivated_account.html",
                      {"activate_account_form": activate_account_form,
                       "reg_form": reg_form,
                       "auth_form": auth_form})


class HelpClientView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        help_client_form = HelpClientForm()
        extra_bar = "Tickets"
        context = {
            "help_client_form": help_client_form,
            "extra_bar": extra_bar,
        }
        return render(request, "User/tickets.html", context)

    def post(self, request):
        help_client_form = HelpClientForm(request.POST)
        if help_client_form.is_valid():
            subject = "Help for client"
            from_email = help_client_form.cleaned_data["email"]
            message = help_client_form.cleaned_data["message"]
            if from_email == request.user.email:
                try:
                    send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER], fail_silently=True)
                    sent = True
                except BadHeaderError:
                    return HttpResponse('???????????? ?? ???????? ????????????.')
                return redirect('success')
            else:
                messages.error(request, 'Your email is wrong')
        return render(request, "User/tickets.html", {"help_client_form": help_client_form})


class HelpCheckStatusOfMYOrderView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Check status of my order"
        return render(request, "User/help_support/check_status_of_my_order.html", {"extra_bar": extra_bar})


class HelpChangeItemsOfMyOrderView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Change Items Of My Order"
        return render(request, "User/help_support/change_items_of_my_order.html", {"extra_bar": extra_bar})


class HelpCancelMYOrderView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Cancel My Order"
        return render(request, "User/help_support/cancel_my_order.html", {"extra_bar": extra_bar})


class HelpChangeMyDeliveryAddressView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Change My Delivery Address"
        return render(request, "User/help_support/change_my_delivery_address.html", {"extra_bar": extra_bar})


class HelpPickUpOrderView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Pick-Up Order"
        return render(request, "User/help_support/help_with_a_pick-up_order.html", {"extra_bar": extra_bar})


class HelpDeliveryPersonMadeUnsafeView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Delivery Person Made Unsafe"
        return render(request, "User/help_support/my_delivery_person_made_me_unsafe.html", {"extra_bar": extra_bar})


class HelpRefundingPaymentView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Refunding Payment"
        return render(request, "User/help_support/refunding_payment.html", {"extra_bar": extra_bar})


class SignUpView(View):
    def get(self, request):
        reg_form = UserRegistrationForm()
        promos = PromoCode.objects.all()
        context = {
            "reg_form": reg_form,
            "promos": promos,
        }
        return render(request, "User/sign_up_page.html", context)

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


class SignInView(View):
    def get(self, request):
        gt = request.GET
        print(gt.get('r1'))
        auth_form = UserAuthenticationForm()
        context = {
            "auth_form": auth_form
        }
        return render(request, "User/sign_in_page.html", context)

    def post(self, request):
        gt = request.POST.get('r1')
        print(gt)
        print(request.POST.get('r2'))
        print(request.POST.get('sum'))
        auth_form = UserAuthenticationForm(request.POST)
        if auth_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('user_page_my_account', user.email)
        else:
            print(auth_form.errors)


class HelpSupportNotLogIn(View):
    def get(self, request):
        extra_bar = "Help & Support"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in.html",
                      {"extra_bar": extra_bar, "reg_form": reg_form, "auth_form": auth_form})

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


class HelpCheckStatusOfMYOrderNotLogInView(View):
    def get(self, request):
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        extra_bar = "Check Status Of My Order"
        return render(request, "User/help_support_not_log_in/check_status_of_my_order_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpChangeItemsOfMyOrderNotLogInView(View):
    def get(self, request):
        extra_bar = "Change Items Of My Order"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/change_items_of_my_order_not_log_in.html",
                      {"extra_bar": extra_bar, "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpCancelMYOrderNotLogInView(View):
    def get(self, request):
        extra_bar = "Cancel My Order"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/cancel_my_order_not_log_in.html", {"extra_bar": extra_bar,
                                                                                                "reg_form": reg_form,
                                                                                                "auth_form": auth_form})

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


class HelpChangeMyDeliveryAddressNotLogInView(View):
    def get(self, request):
        extra_bar = "Change My Delivery"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/change_my_delivery_address_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpPickUpOrderNotLogInView(View):
    def get(self, request):
        extra_bar = "PickUpOrder"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/help_with_a_pick-up_order_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpDeliveryPersonMadeUnsafeNotLogInView(View):
    def get(self, request):
        extra_bar = "Delivery Person Made Me Unsafe"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/my_delivery_person_made_me_unsafe_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpRefundingPaymentNotLogInView(View):
    def get(self, request):
        extra_bar = "Refunding Payment"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/help_support_not_log_in/refunding_payment_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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


class HelpClientNotLogInView(View):

    def get(self, request):
        help_client_form = HelpClientForm()
        extra_bar = "Help Client"
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        context = {
            "help_client_form": help_client_form,
            "extra_bar": extra_bar,
            "reg_form": reg_form,
            "auth_form": auth_form,
        }
        return render(request, "User/ticket_not_log_in.html", context)

    def post(self, request):
        help_client_form = HelpClientForm(request.POST)
        reg_form = UserRegistrationForm(request.POST)
        auth_form = UserAuthenticationForm(request.POST)
        if help_client_form.is_valid():
            subject = "Help for client"
            from_email = help_client_form.cleaned_data["email"]
            message = help_client_form.cleaned_data["message"]
            if from_email == request.user.email:
                try:
                    send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER], fail_silently=True)
                    sent = True
                except BadHeaderError:
                    return HttpResponse('???????????? ?? ???????? ????????????.')
                return redirect('success')
            else:
                return HttpResponse('???????????????????????? email.')

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
        return render(request, "User/ticket_not_log_in", {"help_client_form": help_client_form, "reg_form": reg_form,
                                                          "auth_form": auth_form, })


class HelpTermsConditionsView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Terms & Conditions"
        return render(request, "User/terms_privacy/terms_conditions.html", {"extra_bar": extra_bar})


class HelpPrivacyView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "Privacy"
        return render(request, "User/terms_privacy/privacy.html", {"extra_bar": extra_bar})


class HelpPrivacyNotLogInView(View):
    def get(self, request):
        extra_bar = "Privacy"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/terms_privacy_not_log_in/privacy_not_log_in.html", {"extra_bar": extra_bar,
                                                                                         "reg_form": reg_form,
                                                                                         "auth_form": auth_form})

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


class FAQView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        extra_bar = "FAQ"
        return render(request, "User/terms_privacy/faq.html", {"extra_bar": extra_bar})


class FAQNotLogInView(View):
    def get(self, request):
        extra_bar = "FAQ"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/terms_privacy_not_log_in/faq_not_log_in.html",
                      {"extra_bar": extra_bar, "reg_form": reg_form,
                       "auth_form": auth_form})

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


class TermsPrivacyNotLogIn(View):
    def get(self, request):
        extra_bar = "Terms & Privacy"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/terms_privacy_not_log_in.html",
                      {"extra_bar": extra_bar, "reg_form": reg_form, "auth_form": auth_form})

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


class HelpTermsConditionsNotLogInView(View):
    def get(self, request):
        extra_bar = "Terms & Conditions"
        reg_form = UserRegistrationForm()
        auth_form = UserAuthenticationForm()
        return render(request, "User/terms_privacy_not_log_in/terms_conditions_not_log_in.html",
                      {"extra_bar": extra_bar,
                       "reg_form": reg_form,
                       "auth_form": auth_form})

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
