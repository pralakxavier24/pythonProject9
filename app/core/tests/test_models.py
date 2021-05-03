from django.test import TestCase
from django.contrib.auth import get_user_model
from app.core import models

def sample_user(email="pralakxavier@gmail.com",password="123456"):
    return get_user_model().objects.create_user(email,password)

class ModelTest(TestCase):

    def test_create_email_successful(self):
        email = "pralakxavier@gmail.com"
        password = '12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalize(self):
        email = 'PralakXavier.com'
        user = get_user_model().objects.create_user(
            "pralakxavier.com", '12345'
        )

        self.assertEqual(user.email, email.lower())

    def test_email_Invalid_Email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None, '12345'
            )

    def test_is_superuser(self):
        user = get_user_model().objects.create_superuser(
            'pralakxavier@gmail.com',
            '12345'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = "vegan"
        )
        self.assertEqual(str(tag),tag.name)

