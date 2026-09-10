from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.user_change_password, name="user_change_password"),

    # Password reset (forgot password)
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Password reset via security question
    path('password-reset-question/', views.password_reset_username, name='password_reset_question'),
    path('password-reset-question/<str:username>/', views.password_reset_question, name='password_reset_question_user'),
]