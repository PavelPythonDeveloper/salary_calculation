from django.test import TestCase
from django.urls import reverse
from .models import Event
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def create_event(title, comment, date_of_the_event, price):
    creator = User()
    creator.save()
    # print(creator)
    event = Event.objects.create(title=title,
                                 comment=comment,
                                 date_of_the_event=date_of_the_event,
                                 price=price,
                                 creator=creator)
    return event


class EventEventsListViewTest(TestCase):
    def test_no_events(self):
        """
        If no events exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('events:events_list', kwargs={'user_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no event. Add one?')
        self.assertQuerySetEqual(response.context['events'], [])


class EventEventsDetailViewTest(TestCase):
    def test_event_detail_is_available(self):
        create_event(title='Testing',
                     comment='We test our code sometimes',
                     date_of_the_event=timezone.now() + timedelta(days=3),
                     price=1000
                     )
        response = self.client.get(reverse('events:events_detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testing')
        self.assertContains(response, 'We test our code sometimes')
        self.assertContains(response, '1000')
