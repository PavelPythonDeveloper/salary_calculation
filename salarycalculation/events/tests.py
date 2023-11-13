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
    def test_no_events(self):
        """
        If user has no events, an appropriate message is displayed.
        """
        User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')
        response = self.client.get(reverse('events:events_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no event. Add one?')
        self.assertQuerySetEqual(response.context['events'], [])


class EventEventsDetailViewTest(TestCase):
    def test_event_detail_is_available(self):
        user = User.objects.create_user(username='tester', password='12345')
        logged_in = self.client.login(username='tester', password='12345')
        event = create_event(title='Testing',
                             comment='We test our code sometimes',
                             date_of_the_event=timezone.now() + timedelta(days=3),
                             price=1000,
                             creator=user)

        response = self.client.get(reverse('events:events_detail', kwargs={'id': event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testing')
        self.assertContains(response, 'We test our code sometimes')
        self.assertContains(response, '1000')

        
