from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from .views import index2, HomePage, UserPage, logout_view, DeactivateAccountView, DeleteAccount, ForgotPassword, \
    password_reset_request, contact_view, success, ChangePassword, TermsConditionsView, HelpSupportView, TicketView, \
    AddressView, AvailablePromosView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('index', index2, name='index2'),
    path('user_page_my_account/<str:email>', UserPage.as_view(), name="user_page_my_account"),
    path('user_page_change_password/<str:email>', ChangePassword.as_view(), name="user_page_change_password"),
    path('logout', logout_view, name='logout'),
    path('deactivate', DeactivateAccountView.as_view(), name='deactivate'),
    path('delete_account', DeleteAccount.as_view(), name='delete_account'),
    path('terms_conditions', TermsConditionsView.as_view(), name='terms_conditions'),
    path('available_promos', AvailablePromosView.as_view(), name='available_promos'),
    path('ticket', TicketView.as_view(), name='ticket'),
    path('address', AddressView.as_view(), name='address'),
    path('help_support', HelpSupportView.as_view(), name='help_support'),
    path('forgot_password', ForgotPassword.as_view(), name='forgot_password'),
    # path('password_reset', password_reset_request, name="password_reset"),
    path('password_reset', PasswordResetView.as_view(
        # template_name="User/forgot_password.html"
    ), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact', contact_view, name="contact"),
    path('success', success, name='success'),
    # path('change_password', PasswordChangeView.as_view(template_name="User/change_password.html"),
    #      name='change_password'),

    path('<str:name>', HomePage.as_view(), name='home_page'),

]
