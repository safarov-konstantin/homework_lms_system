from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentListAPIView
from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentCreateAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    # payments
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='course-payment'),
    # aut jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # model user
    path('', UserListAPIView.as_view(), name='users'),
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
]
