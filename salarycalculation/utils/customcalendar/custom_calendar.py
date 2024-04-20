from django.utils import timezone
import calendar

January = 1


class CustomHTMLCal(calendar.HTMLCalendar):
    # CSS class for the month's head
    cssclass_month_head = "month-head"

    # CSS class for the month
    cssclass_month = "month"

    # CSS class for current month
    cssclass_current_month = "current-month"

    cssclass_year_head = "year-head"

    def formatday(self, day, weekday, theyear, themonth, events=None):
        """
        Return a day as a table cell.
        """
        events = events.filter(date_of_the_event__day=day)
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            if events:
                if theyear == timezone.now().year and themonth == timezone.now().month and day == timezone.now().day:
                    return '<td class="%s"><div class="event-calendar-item"><a href="/events/list/?year=%s&month=%s&day=%s"><div class="today" >%d</div></a></div></td>' % (
                        self.cssclasses[weekday], theyear, themonth, day, day)
                return '<td class="%s"><div class="event-calendar-item"><a href="/events/list/?year=%s&month=%s&day=%s">%d</a></div></td>' % (
                    self.cssclasses[weekday], theyear, themonth, day, day)
            else:
                if theyear == timezone.now().year and themonth == timezone.now().month and day == timezone.now().day:
                    return '<td class="%s"><div style="margin: 10px;"><div class="today"><a href="/events/create/?year=%s&month=%s&day=%s" >%d</a></div></div></td>' % (
                        self.cssclasses[weekday], theyear, themonth, day, day)
                return '<td class="%s"><div style="margin: 10px;"><a href="/events/create/?year=%s&month=%s&day=%s" >%d</a></div></td>' % (
                    self.cssclasses[weekday], theyear, themonth, day, day)

    def formatweek(self, theweek, theyear, themonth, events=None):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, theyear, themonth, events=events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True, events=None):
        """
        Return a formatted month as a table.
        """
        events = events.filter(date_of_the_event__month=themonth)
        v = []
        a = v.append
        if themonth == timezone.now().month and theyear == timezone.now().year:
            a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
                self.cssclass_current_month))
        else:
            a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
                self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear, themonth, events=events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, theyear=timezone.now().year, width=3, events=None):
        """
        Return a formatted year as a table of tables.
        """
        previous_year = theyear - 1
        next_year = theyear + 1
        form = "<form id='year-switch' action='/events/calendar/' method='get'></form>"
        previous = "<input form='year-switch' class='button' name='year' value='%s' type='submit'>" % (previous_year)
        next = "<input form='year-switch' class='button' name='year' value='%s' type='submit'>" % (next_year)

        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' %
          self.cssclass_year)
        a('\n')
        a('<tr><th colspan="%d" class="" >%s<div style="display: flex; justify-content: center; margin: 30px 0 30px 0;">%s <div class="button">%s</div> %s</div></th></tr>' % (
            width, form, previous, theyear, next))
        for i in range(January, January + 12, width):
            # months in this row
            months = range(i, min(i + width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(theyear, m, withyear=False, events=events))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)
