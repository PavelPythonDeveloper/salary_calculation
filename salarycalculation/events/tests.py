from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from .models import Event
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def create_event(title, comment, date_of_the_event, price, creator):
    event = Event.objects.create(title=title,
                                 comment=comment,
                                 date_of_the_event=date_of_the_event,
                                 price=price,
                                 creator=creator)

    return event


class EventEventsListViewTest(TestCase):
    def setUp(self):
        """
        Create and login test user
        """
        User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')

    def test_no_event_exists(self):
        """
        If user has no events, an appropriate message is displayed.
        """
        response = self.client.get(reverse('events:events_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no event. Add one?')
        self.assertQuerySetEqual(response.context['events'], [])

    def test_unlogged_user_access(self):
        """
        If unlogged user tries access to Event list he redirects to log-in
        """
        self.client.logout()
        response = self.client.get(reverse('events:events_list'))
        self.assertRedirects(response, '/users/login/?next=/events/list/', status_code=302, target_status_code=200)


class EventEventsDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')
        self.event = create_event(title='Testing',
                                  comment='We test our code sometimes',
                                  date_of_the_event=timezone.now() + timedelta(days=3),
                                  price=1000,
                                  creator=user)

    def test_event_detail_is_available(self):
        response = self.client.get(reverse('events:events_detail', kwargs={'id': self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testing')
        self.assertContains(response, 'We test our code sometimes')
        self.assertContains(response, '1000')


class EventCalculateViewTest(TestCase):
    def setUp(self):
        username = 'tester'
        password = '12345'
        user = User.objects.create_user(username=username, password=password)
        titles = ['title1', 'title2', 'title3', 'title4', 'title5', 'title6', 'title7', 'title8', 'title9', 'title10']
        price = 500
        creator = user
        date_of_the_event = timezone.now() - timedelta(days=4)
        self.client.login(username=username, password=password)
        for num in range(10):
            create_event(title=titles[num],
                         comment='comment',
                         date_of_the_event=date_of_the_event + timedelta(days=num),
                         price=price,
                         creator=creator)

    def test_calculate_is_available(self):
        response = self.client.get(reverse('events:calculate'))
        self.assertEqual(response.status_code, 200)

