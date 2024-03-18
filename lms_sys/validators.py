from rest_framework import serializers


class VideoValitator:
    def __call__(self, value):
        if value is None:
            pass
        elif not 'youtube.com' in value:
            raise serializers.ValidationError("Запрещено использовать ссылки на ресурсы, кроме 'youtube.com'")
