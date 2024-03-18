from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsModerator

from lms_sys.serializers import CourseSerializer, LessonSerializer
from lms_sys.models import Course, Lesson, Subscription
from lms_sys.permissions import IsOwner
from lms_sys.paginators import MyPagination


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_queryset(self):
        qs = Course.objects.all()
        if not self.request.user.is_moderator:
            qs = qs.filter(owner=self.request.user)
        return qs

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'create':
            permission_classes = [~IsModerator]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MyPagination

    def get_queryset(self):
        if not self.request.user.is_moderator:
            self.queryset = self.queryset.filter(owner=self.request.user)
        return super().get_queryset()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdataAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionAPIView(APIView):
    def post(self, request, pk):
        user = request.user
        course = generics.get_object_or_404(Course, id=pk)
        subs_item, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            message = 'Подписка добавлена'
        else:
            subs_item.delete()
            message = 'Подписка удалена'

        return Response({"message": message})