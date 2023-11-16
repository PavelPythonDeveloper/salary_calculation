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
    def test_no_event_exists(self):
        """
        If user has no events, an appropriate message is displayed.
        """
        User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')
        response = self.client.get(reverse('events:events_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no event. Add one?')
        self.assertQuerySetEqual(response.context['events'], [])

    def test_unlogged_user_access(self):
        """
        If unlogged user tries access to Event list he redirects to log-in
        """
        User.objects.create_user(username='tester', password='12345')
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

# class EventCalculateViewTest(TestCase):
#     def test_calculate_is_available(self):
#
#         user = User.objects.create_user(username='tester', password='12345')
#         logged_in = self.client.login(username='tester', password='12345')
#         event1 = create_event(title='event1', price=1000, creator=user)
#         event2 = create_event(title='event2', price=1000, creator=user)
#         event3 = create_event(title='event3', price=1000, creator=user)
#         event4 = create_event(title='event4', price=1000, creator=user)
