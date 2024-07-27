from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer


class CustomUserTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@case.com",
            "name": "Test",
            "surname": "Case",
            "password": "test"
        }
        self.superuser_data = {
            "email": "test-super@case.com",
            "name": "Super",
            "surname": "Case",
            "password": "test"
        }

    def test_create_user(self):
        initial_user_count = CustomUser.objects.count()
        serializer = CustomUserSerializer(data=self.user_data)
        serializer.is_valid()
        user = serializer.save()
        final_user_count = CustomUser.objects.count()

        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertEqual(user.surname, self.user_data['surname'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertNotEqual(initial_user_count, final_user_count)

    def test_user_update_positive(self):
        serializer = CustomUserSerializer(data=self.user_data)
        serializer.is_valid()
        user = serializer.save()
        initial_user_count = CustomUser.objects.count()
        new_data = {
            "email": "test2@case.com",
            "name": "Test2",
            "surname": "Case2",
            "password": "test2"
        }
        serializer = CustomUserSerializer(instance=user, data=new_data)
        serializer.is_valid()
        updated_user = serializer.save()
        final_user_count = CustomUser.objects.count()

        self.assertEqual(updated_user.email, new_data['email'])
        self.assertEqual(updated_user.name, new_data['name'])
        self.assertEqual(updated_user.surname, new_data['surname'])
        self.assertTrue(updated_user.check_password(new_data['password']))
        self.assertEqual(initial_user_count, final_user_count)

    def test_user_update_negative(self):
        new_data = {
            "email": "test2.case.com",
            "name": "Test2",
            "surname": "Case2",
            "password": "test2"
        }
        serializer = CustomUserSerializer(data=self.user_data)
        serializer.is_valid()
        user = serializer.save()
        serializer = CustomUserSerializer(instance=user, data=new_data)

        self.assertFalse(serializer.is_valid())

    def test_get_user_detail(self):
        self.url = reverse('user-detail')
        serializer = CustomUserSerializer(data=self.user_data)
        serializer.is_valid()
        self.user = serializer.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        expected_data = CustomUserSerializer(instance=self.user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_user_by_id(self):
        n = 5
        initial_user_count = CustomUser.objects.count()
        for i in range(n):
            self.user_data['email'] = f"test{i}@case.com"
            serializer = CustomUserSerializer(data=self.user_data)
            serializer.is_valid()
            serializer.save()
        self.user = serializer.save()

        self.client.force_authenticate(user=self.user)
        self.url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(self.url)
        final_user_count = CustomUser.objects.count()
        expected_data = {
            "id": self.user.id,
            "email": f"test{n - 1}@case.com",
            "name": "Test",
            "surname": "Case",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(initial_user_count, final_user_count - n)

    def test_get_all_users_detail_auth(self):
        initial_user_count = CustomUser.objects.count()
        serializer = CustomUserSerializer(data=self.user_data)
        serializer.is_valid()
        serializer.save()
        self.user = serializer.save()
        CustomUser.objects.create_superuser(**self.superuser_data)
        final_user_count = CustomUser.objects.count()

        self.client.force_authenticate(user=self.user)
        self.url = reverse('all-users')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_create_superuser(self):
        super_user = CustomUser.objects.create_superuser(**self.superuser_data)

        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_active)
