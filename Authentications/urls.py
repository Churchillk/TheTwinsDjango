from django.urls import path
from . import views as UserViews
from django.contrib.auth import views as auth_view

urlpatterns = [
    # path("register/", UserViews.register, name='register'),
    path("login/", UserViews.CustomLoginView.as_view(), name='login'),
    path("profile/", UserViews.Profile.as_view(), name="profile"),
    path("profile/edit/", UserViews.ProfileUpdateView.as_view(), name="profile_update"),
    path('logout/', UserViews.MainLogoutView.as_view(next_page="login"), name='logout'),
    path('admin-logout/', UserViews.AdminLogoutView.as_view(next_page="admin_login"), name='admin_logout'),
    path("password_reset/done", auth_view.PasswordResetDoneView.as_view(template_name="Users/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name="Users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", auth_view.PasswordResetCompleteView.as_view(template_name="Users/password_reset_complete.html"), name="password_reset_complete"),
]