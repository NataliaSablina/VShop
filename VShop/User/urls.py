from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from .views import index2, HomePageView, UserPageView, logout_view, DeactivateAccountView, DeleteAccountView, \
    ForgotPasswordView, \
    password_reset_request, contact_view, success, ChangePasswordView, TermsConditionsView, AddressView, \
    ActivateAccountView, \
    HelpClientView, HelpSupportView, HelpCheckStatusOfMYOrderView, HelpChangeItemsOfMyOrderView, HelpCancelMYOrderView, \
    HelpChangeMyDeliveryAddressView, HelpPickUpOrderView, HelpDeliveryPersonMadeUnsafeView, HelpRefundingPaymentView, \
    SendMailSuccess, SignUpView, SignInView, HelpSupportNotLogIn, HelpCheckStatusOfMYOrderNotLogInView, \
    HelpChangeItemsOfMyOrderNotLogInView, HelpCancelMYOrderNotLogInView, HelpChangeMyDeliveryAddressNotLogInView, \
    HelpPickUpOrderNotLogInView, HelpDeliveryPersonMadeUnsafeNotLogInView, HelpRefundingPaymentNotLogInView, \
    HelpClientNotLogInView, HelpTermsConditionsView, HelpPrivacyView, FAQView, TermsPrivacyNotLogIn, \
    HelpTermsConditionsNotLogInView, HelpPrivacyNotLogInView, FAQNotLogInView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView



urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('index', index2, name='index2'),
    path('user_page_my_account/<str:email>', UserPageView.as_view(), name="user_page_my_account"),
    path('user_page_change_password/<str:email>', ChangePasswordView.as_view(), name="user_page_change_password"),
    path('logout', logout_view, name='logout'),
    path('sign_up_page', SignUpView.as_view(), name='sign_up_page'),
    path('sign_in_page', SignInView.as_view(), name='sign_in_page'),
    path('help_support_not_log_in', HelpSupportNotLogIn.as_view(), name='help_support_not_log_in'),
    path('deactivate', DeactivateAccountView.as_view(), name='deactivate'),
    path('delete_account', DeleteAccountView.as_view(), name='delete_account'),
    path('terms_conditions', TermsConditionsView.as_view(), name='terms_conditions'),
    path('ticket', HelpClientView.as_view(), name='ticket'),
    path('ticket_not_log_in', HelpClientNotLogInView.as_view(), name='ticket_not_log_in'),
    path('check_status_of_my_order', HelpCheckStatusOfMYOrderView.as_view(), name='check_status_of_my_order'),
    path('check_status_of_my_order_not_log_in', HelpCheckStatusOfMYOrderNotLogInView.as_view(), name='check_status_of_my_order_not_log_in'),
    path('change_items_of_my_order', HelpChangeItemsOfMyOrderView.as_view(), name='change_items_of_my_order'),
    path('change_items_of_my_order_not_log_in', HelpChangeItemsOfMyOrderNotLogInView.as_view(), name='change_items_of_my_order_not_log_in'),
    path('cancel_my_order', HelpCancelMYOrderView.as_view(), name='cancel_my_order'),
    path('cancel_my_order_not_log_in', HelpCancelMYOrderNotLogInView.as_view(), name='cancel_my_order_not_log_in'),
    path('change_my_delivery_address', HelpChangeMyDeliveryAddressView.as_view(), name='change_my_delivery_address'),
    path('change_my_delivery_address_not_log_in', HelpChangeMyDeliveryAddressNotLogInView.as_view(), name='change_my_delivery_address_not_log_in'),
    path('help_with_a_pick-up_order', HelpPickUpOrderView.as_view(), name='help_with_a_pick-up_order'),
    path('help_with_a_pick-up_order_not_log_in', HelpPickUpOrderNotLogInView.as_view(), name='help_with_a_pick-up_order_not_log_in'),
    path('my_delivery_person_made_me_unsafe', HelpDeliveryPersonMadeUnsafeView.as_view(), name='my_delivery_person_made_me_unsafe'),
    path('my_delivery_person_made_me_unsafe_not_log_in', HelpDeliveryPersonMadeUnsafeNotLogInView.as_view(), name='my_delivery_person_made_me_unsafe_not_log_in'),
    path('refunding_payment', HelpRefundingPaymentView.as_view(), name='refunding_payment'),
    path('refunding_payment_not_log_in', HelpRefundingPaymentNotLogInView.as_view(), name='refunding_payment_not_log_in'),
    path('address', AddressView.as_view(), name='address'),
    path('help_support', HelpSupportView.as_view(), name='help_support'),
    path('forgot_password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('terms_conditions_user', HelpTermsConditionsView.as_view(), name='terms_conditions_user'),
    path('terms_conditions_not_log_in', HelpTermsConditionsNotLogInView.as_view(), name='terms_conditions_not_log_in'),
    path('privacy', HelpPrivacyView.as_view(), name='privacy'),
    path('privacy_not_log_in', HelpPrivacyNotLogInView.as_view(), name='privacy_not_log_in'),
    path('faq', FAQView.as_view(), name='faq'),
    path('faq_not_log_in', FAQNotLogInView.as_view(), name='faq_not_log_in'),
    path('terms_privacy_not_log_in', TermsPrivacyNotLogIn.as_view(), name='terms_privacy_not_log_in'),
    path('send_mail_success', SendMailSuccess.as_view(), name='send_mail_success'),
    # path('password_reset', password_reset_request, name="password_reset"),
    path('password_reset', contact_view, name="password_reset"),
    # path('password_reset', PasswordResetView.as_view(
    #     # template_name="User/forgot_password.html"
    # ), name='password_reset'),
    # path('password_reset/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name="User/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/complete', PasswordResetCompleteView.as_view(template_name="User/password_reset_complete.html"), name='password_reset_complete'),
    # path('contact', contact_view, name="contact"),
    path('success', success, name='success'),
    path('activate_account', ActivateAccountView.as_view(), name='activate_account'),
    # path('change_password', PasswordChangeView.as_view(template_name="User/change_password.html"),
    #      name='change_password'),

    path('<str:name>', HomePageView.as_view(), name='home_page'),

]
