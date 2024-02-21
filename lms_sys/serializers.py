from rest_framework import serializers
from lms_sys.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        lesson_instance = instance.lesson.all()
        if lesson_instance:
            return lesson_instance.count()
        return 0
