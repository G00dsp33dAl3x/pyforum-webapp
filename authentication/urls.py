from django.urls import path
from .views import CreateUserView, UserDetailView, UsersDetailView, AllUsersDetailView # CustomPasswordReset
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as djauth

urlpatterns = [
    path('api/register/', CreateUserView.as_view(), name='user-create'),
    path('api/user/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/users/<int:id>', UsersDetailView.as_view(), name='users-detail'),
    path('api/users/all/', AllUsersDetailView.as_view(), name='all-users'),
    # path('api/user/passwordreset/', CustomPasswordReset.as_view(), name='password-reset'),
    # path('api/user/passwordreset/confirm/<uidb64>/<token>/', djauth.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('api/password_reset/done/', djauth.PasswordResetDoneView.as_view(), name='password_reset_done'),
]


