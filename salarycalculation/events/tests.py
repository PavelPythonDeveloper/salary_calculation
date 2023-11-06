from django.test import TestCase
from django.urls import reverse


class EventEventsListViewTest(TestCase):
    def test_no_events(self):
        """
        If no events exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('events:events_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no event. Add one?')
        self.assertQuerySetEqual(response.context['events'], [])
