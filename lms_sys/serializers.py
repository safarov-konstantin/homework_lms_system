from rest_framework import serializers

from lms_sys.models import Course, Lesson, Subscription
from lms_sys.validators import VideoValitator


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[VideoValitator()])
    
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        lesson_instance = instance.lesson.all()
        if lesson_instance:
            return lesson_instance.count()
        return 0

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        elif user.is_superuser:
            return False
        elif user.is_moderator:
            return False
        else:
            return Subscription.objects.filter(user=user, course=instance).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
