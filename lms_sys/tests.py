from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from lms_sys.models import Lesson, Course


class LessonAPITestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, email="test@test.ru", password='passwd')
        self.client.force_authenticate(user=self.user)
        
        self.course = Course.objects.create(
                id=1,
                name='course_test',
                description='course_test',
                owner=self.user
        )
        
        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test_lesson",
            course=self.course,
            owner=self.user
        )

    def test_lessson_create(self):
        data = {
            "name" : "test_lesson_2",
            "description": "test_lesson_2",
            "course": self.course.id,
            "owner": self.user.id,
            "video": r"https://www.youtube.com/4567"
        }
        response = self.client.post(reverse('lms_sys:lessson-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(pk=response.json()['id']).exists())

    def test_lessson_list(self):
        response = self.client.get(reverse('lms_sys:lessson-list'))        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.id,
                        'video': None,
                        'name': 'test_lesson',
                        'description': 'test_lesson',
                        'preview': None,
                        'course': 1,
                        'owner': 1
                    }
                ]
            }
        )

    def test_lessson_get(self):
        response = self.client.get(
            reverse('lms_sys:lessson-get', kwargs={'pk': self.lesson.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.pk,
                'video': None,
                'name': 'test_lesson',
                'description': 'test_lesson',
                'preview': None,
                'course': self.course.id,
                'owner': self.user.id
            }
        )

    def test_lesson_update(self):
        data = {
            "name": "test_update",
            "description": "test_update",
            "course": self.course.id,
        }
        response = self.client.patch(
            reverse('lms_sys:lessson-update',kwargs={'pk': self.lesson.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'video': None,
                'name':'test_update',
                'description': 'test_update',
                'preview': None,
                'course': self.course.id,
                'owner': self.user.id
            }
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            reverse('lms_sys:lessson-delete', kwargs={'pk': self.lesson.pk}),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )    


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(id=1, email="test@test.ru", password='passwd')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
                id=1,
                name='course_test',
                description='course_test',
                owner=self.user
        )

    def test_create_subscription(self):
        response = self.client.post(
            reverse("lms_sys:subscribe", kwargs={'pk': self.course.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'message': 'Подписка добавлена'}
        )
