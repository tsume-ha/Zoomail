from django.test import TestCase, Client
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
import datetime


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    user = User.objects.create_user(
        email = str(year) + 'mail@gmail.com',
        year = year
        )
    user.first_name = str(year) + '名前'
    user.last_name = str(year) + '名字'
    user.furigana = 'ふりがな'
    user.receive_email = str(year) + 'mail@gmail.com'
    user.save()
    return user

def Force_Login(self, year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client = Client()
    self.client.force_login(user)
    return user

def Make_a_Calendar(self, year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    calendar = Calendar.objects.create(
        title = 'テストバンド',
        created_by = user,
        days_begin = datetime.datetime.now(),
        days_end = datetime.datetime.now() + datetime.timedelta(days=30),
        invite_key = 'invitation_key',
        )
    date = calendar.days_begin
    while date <= calendar.days_end:
        date_calendar = CollectHour(
            calendar=calendar,
            date=date,
            hour_begin=9,
            hour_end=26,
            )
        date_calendar.save()
        date = date + datetime.timedelta(days=1)
    CalendarUser.objects.create(
        calendar=calendar, user=user
        )
    return calendar

def logOUT_test_view(self, url):
    User_LogOUT(self)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)
    url_redial_to = response.url
    response = self.client.get(url_redial_to)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'admin/login.html')
    return response

def logIN_test_view(self, calendar, url):
    Force_Login(self)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    User_LogOUT(self)

    user = Make_User(self, year=2018)
    Force_Login(self, year=2018)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)

    CalendarUser.objects.create(
        calendar=calendar, user=user
        )
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    return response


class CalendarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_awase_index_logOUT(self):
        url = '/awase/'
        logOUT_test_view(self, url=url)

    def test_awase_index_logIN(self):
        Force_Login(self)
        response = self.client.get('/awase/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/index.html')

    def test_awase_create_logOUT(self):
        url = '/awase/create/'
        logOUT_test_view(self, url=url)

    def test_awase_create_logIN(self):
        url = '/awase/create/'
        Force_Login(self)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/create.html')

    def test_awase_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/calendar.html')

    def test_awase_input_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/%s/input/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_input_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/%s/input/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/input.html')

    def test_awase_update_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/calendar/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/calendar/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_calendar.html')

    def test_awase_update_hours_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/hours/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_hours_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/hours/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_hours.html')

    def test_awase_update_urlkey_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/urlkey/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_urlkey_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/urlkey/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_URLKey.html')

    def test_awase_update_user_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/user/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_user_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/update/user/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/change_users.html')

    def test_awase_leave_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/leave/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_leave_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/leave/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/leave_calendar.html')

    def test_awase_delete_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/delete/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_delete_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/delete/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/delete_calendar.html')


class CalendarCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_create_calendar_POST_logOUT(self):
        data = {
            
        }

        # request = self.client.post('/send/', data)