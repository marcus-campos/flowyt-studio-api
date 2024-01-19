from django.urls import re_path


from . import views


urlpatterns = [
    re_path(r"^register/$", views.UserRegistrationAPIView.as_view(), name="register"),
    re_path(
        r"^verify/(?P<verification_key>.+)/$",
        views.UserEmailVerificationAPIView.as_view(),
        name="email_verify",
    ),
    re_path(r"^password_reset/$", views.PasswordResetAPIView.as_view(), name="password_change",),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    re_path(r"^user-profile/$", views.UserProfileAPIView.as_view(), name="user_profile"),
]
