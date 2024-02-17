from lms_sys.apps import LmsSysConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from lms_sys.views import(
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdataAPIView
)

app_name = LmsSysConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessson/create/', LessonCreateAPIView.as_view(), name='lessson-create'),
    path('lesssons/', LessonListAPIView().as_view(), name='lessson-list'),
    path('lessson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessson-get'),
    path('lessson/update/<int:pk>/', LessonUpdataAPIView.as_view(), name='lessson-update'),
    path('lessson/delet/<int:pk>/', LessonDestroyAPIView.as_view(), name='lessson-delete'),
] + router.urls