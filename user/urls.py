from django.urls import path
from .views import UserCreateView, CustomTokenObtainPairView,GoogleLoginView, UserListView, UserDetailView, CurrentUserView, GoogleLoginCallback, google_login_callback, validate_google_token, GoogleLogin, GoolgeLoginAPI
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include, path, re_path

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name = 'create-user'),
    path('list-user/', UserListView.as_view(), name = 'list-user'),
    path('current/', CurrentUserView.as_view(), name = 'current-user'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('list-user/<int:pk>', UserDetailView.as_view(), name = 'list-current-user'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token-obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path(
    #     "api/v1/auth/google/callback/",
    #     GoogleLoginCallback.as_view(),
    #     name="google_login_callback",
    # ),
    # path('callback/', google_login_callback, name='callback'),
    # path('api/google/validate_token', validate_google_token, name='validate_token'),

    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "api/v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    path('api/v1/auth/login/google/', GoolgeLoginAPI.as_view(), name='login-with-goolge'),
]