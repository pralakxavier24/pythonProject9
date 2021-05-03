from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succes(self):
        payload = {
            'email':'xavier@gmail.com',
            'password':'12345',
            'name':'xavier'
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        payload = {
            'email': 'xavier@gmail.com',
            'password': '12345',
            'name': 'xavier'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        payload = {
            'email': 'xavier@gmail.com',
            'password': '123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email'],
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token(self):
        payload = {
            'email': 'xavier@gmail.com',
            'password': '12345',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_invalid_token(self):
        create_user(email= 'xavier@gmail.com',password= '12345')
        payload = {
            'email': 'xavier@gmail.com',
            'password': '1234567',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_user_doesnt_exist(self):
        payload = {
            'email': 'xavier@gmail.com',
            'password': '1234567',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nodata_in_fields(self):
        payload = {
            'email': 'xavier@gmail.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    class PrivateUserApiTests(TestCase):
        def setUp(self):
            self.user = create_user(
                email = 'pralakxavier@gmail.com',
                password = '123456',
                name = 'pralak'
            )
            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

        def test_retrieve_profile_success(self):
            res = self.client.get(ME_URL)
            self.assertEqual(res.status_code,status.HTTP_200_OK)

            self.assertEqual(res.data,{
                'name':self.user.name,
                'email':self.user.name
            })

        def test_post_me_not_allowed(self):
            res = self.client.post(ME_URL,{})

            self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_update_user_profile(self):
            payload = {
                'name':'newname','password':'newpassword'
            }

            res = self.client.patch(ME_URL,payload)
            self.user.refresh_from_db()
            self.assertEqual(self.user.name,payload['name'])
            self.assertTrue(self.user.check_password(payload['password']))
            self.assertEqual(res.status_code,status.HTTP_200_OK)

