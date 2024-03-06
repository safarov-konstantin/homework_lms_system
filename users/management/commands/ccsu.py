from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(
            email='admin@admin.ru',
            first_name='admin',
            last_name='admin',
            is_superuser=True,
            is_staff=True,
            phone='',
            city='',
            is_active=True
        )

        user.set_password('q1w2e3r4!')
        user.save()