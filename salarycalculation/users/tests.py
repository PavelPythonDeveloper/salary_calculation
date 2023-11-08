from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UsersRegisterViewTest(TestCase):
    def test_is_new_user_registered(self):
        response = self.client.post(reverse('users:register'), data={
            'username': 'Tester',
            'email': 'tester@testing.te',
            'password1': 'testerpassword',
            'password2': 'testerpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='Tester').exists())
