from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.permissions import IsOwnerUser

from users.services import create_stripe_price, create_stripe_session


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lesson', 'course', 'pay_method']
    ordering_fields = ['date_payment']


class UserCreateAPIView(generics.CreateAPIView):
    """
    Контреллер для создания пользователя
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """
    Контреллер для чтения пользователей
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Контреллер для обновления пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Контреллер для удаления пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def perform_create(self, serializer):
        course = serializer.validated_data.get('course_id')
        if not course:
            raise serializers.ValidationError('Не выбран курс')

        payment = serializer.save()
        stripe_price_id = create_stripe_price(payment)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.save()
