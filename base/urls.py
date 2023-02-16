from django.urls import path

from base.views import (
    deactivate_account_view,
    delete_account_view,
    email_verify_view,
    home_view,
    login_view,
    logout_view,
    password_change_view,
    password_reset_request_view,
    password_reset_view,
    profile_view,
    register_view,
    search_account_view,
    update_view,
)

app_name = "base"

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/<str:user_id>", profile_view, name="profile"),
    path("account_update/", update_view, name="update-profile"),
    path("account_search/", search_account_view, name="search-profile"),
    path("email_verification/<uidb64>/<token>/", email_verify_view, name="email-verify"),
    path("password_change/", password_change_view, name="password-change"),
    path("password_reset_request/", password_reset_request_view, name="password-reset-request"),
    path("password_reset/<uidb64>/<token>/", password_reset_view, name="password-reset"),
    path("user_deactivate/", deactivate_account_view, name="account-deactivate"),
    path("user_delete/", delete_account_view, name="account-delete"),
]
