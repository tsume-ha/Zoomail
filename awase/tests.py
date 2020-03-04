from django.test import TestCase, Client
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
from .forms import CreateCalendarForm, InputScheduleFormSet, UpdateCollectHourFormSet, UserChangeFormSet
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
        url = '/awase/calendar/%s/urlkey/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_urlkey_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/calendar/%s/urlkey/' % str(calendar.pk)
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
            'title': ['test_calendar_group'],
            'text': ['test_calendar_subscription'],
            'days_begin_year': ['2020'],
            'days_begin_month': ['4'],
            'days_begin_day': ['1'],
            'days_end_year': ['2020'],
            'days_end_month': ['4'],
            'days_end_day': ['10'],
        }
        User_LogOUT(self)
        request = self.client.post('/awase/create/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')
        
        self.assertFalse(Calendar.objects.filter(title=data['title'][0]).exists())

    def test_create_calendar_POST_logIN(self):
        data = {
            'title': ['test_calendar_group'],
            'text': ['test_calendar_subscription'],
            'days_begin_year': ['2020'],
            'days_begin_month': ['4'],
            'days_begin_day': ['10'],
            'days_end_year': ['2020'],
            'days_end_month': ['4'],
            'days_end_day': ['20'],
        }
        user = Force_Login(self)
        request = self.client.post('/awase/create/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'awase/create_complete.html')
        
        self.assertTrue(Calendar.objects.filter(title=data['title'][0]).exists())
        self.assertTrue(CalendarUser.objects.filter(user=user).exists())

        calendar = Calendar.objects.get(title=data['title'][0])
        self.assertFalse(CalendarUser.objects.filter(calendar=calendar).exclude(user=user).exists())

        response = self.client.get('/awase/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/index.html')
        self.assertContains(response, data['title'][0])
        self.assertContains(response, data['text'][0])

        User_LogOUT(self)
        other_user = Make_User(self, year=2018)
        Force_Login(self, year=2018)
        response = self.client.get('/awase/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/index.html')
        self.assertNotContains(response, data['title'][0])
        self.assertNotContains(response, data['text'][0])


        self.assertFalse(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.date(
                year = int(data['days_begin_year'][0]),
                month = int(data['days_begin_month'][0]),
                day = int(data['days_begin_day'][0]) - 1
                )
            ).exists())
        for date in range(int(data['days_begin_day'][0]), int(data['days_end_day'][0])):
            self.assertTrue(CollectHour.objects.filter(
                calendar = calendar,
                date = datetime.date(
                    year = int(data['days_end_year'][0]),
                    month = int(data['days_end_month'][0]),
                    day = date
                    )
                ).exists())
        self.assertTrue(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.date(
                year = int(data['days_end_year'][0]),
                month = int(data['days_end_month'][0]),
                day = int(data['days_end_day'][0])
                )
            ).exists())
        self.assertFalse(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.date(
                year = int(data['days_end_year'][0]),
                month = int(data['days_end_month'][0]),
                day = int(data['days_end_day'][0]) + 1
                )
            ).exists())


class CalendarInputTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)
        cls.calendar = Make_a_Calendar(cls)
        cls.url = '/awase/calendar/%s/input/' % str(cls.calendar.pk)
        cls.time_list = [datetime.datetime.combine(datetime.date.today(), datetime.time(00,00,00))\
                      + datetime.timedelta(days=1, hours=9)\
                      + datetime.timedelta(minutes=30*n)
                     for n in range((26-9)*2)]
        cls.data = {
            '0-0-can_attend': ['True'], '0-0-starttime': [cls.time_list[0].strftime('%Y-%m-%d %H:%M:%S')],
            '0-1-can_attend': ['True'], '0-1-starttime': [cls.time_list[1].strftime('%Y-%m-%d %H:%M:%S')],
            '0-2-can_attend': ['True'], '0-2-starttime': [cls.time_list[2].strftime('%Y-%m-%d %H:%M:%S')],
            '0-3-can_attend': ['True'], '0-3-starttime': [cls.time_list[3].strftime('%Y-%m-%d %H:%M:%S')],
            '0-4-can_attend': ['True'], '0-4-starttime': [cls.time_list[4].strftime('%Y-%m-%d %H:%M:%S')],
            '0-5-can_attend': ['True'], '0-5-starttime': [cls.time_list[5].strftime('%Y-%m-%d %H:%M:%S')],
            '0-6-can_attend': ['True'], '0-6-starttime': [cls.time_list[6].strftime('%Y-%m-%d %H:%M:%S')],
            '0-7-can_attend': ['True'], '0-7-starttime': [cls.time_list[7].strftime('%Y-%m-%d %H:%M:%S')],
            '0-8-can_attend': ['True'], '0-8-starttime': [cls.time_list[8].strftime('%Y-%m-%d %H:%M:%S')],
            '0-9-can_attend': ['True'], '0-9-starttime': [cls.time_list[9].strftime('%Y-%m-%d %H:%M:%S')],
            '0-10-can_attend': ['True'], '0-10-starttime': [cls.time_list[10].strftime('%Y-%m-%d %H:%M:%S')],
            '0-11-can_attend': ['True'], '0-11-starttime': [cls.time_list[11].strftime('%Y-%m-%d %H:%M:%S')],
            '0-12-can_attend': ['True'], '0-12-starttime': [cls.time_list[12].strftime('%Y-%m-%d %H:%M:%S')],
            '0-13-can_attend': ['True'], '0-13-starttime': [cls.time_list[13].strftime('%Y-%m-%d %H:%M:%S')],
            '0-14-can_attend': ['True'], '0-14-starttime': [cls.time_list[14].strftime('%Y-%m-%d %H:%M:%S')],
            '0-15-can_attend': ['True'], '0-15-starttime': [cls.time_list[15].strftime('%Y-%m-%d %H:%M:%S')],
            '0-16-can_attend': ['True'], '0-16-starttime': [cls.time_list[16].strftime('%Y-%m-%d %H:%M:%S')],
            '0-17-can_attend': ['True'], '0-17-starttime': [cls.time_list[17].strftime('%Y-%m-%d %H:%M:%S')],
            '0-18-can_attend': ['True'], '0-18-starttime': [cls.time_list[18].strftime('%Y-%m-%d %H:%M:%S')],
            '0-19-can_attend': ['True'], '0-19-starttime': [cls.time_list[19].strftime('%Y-%m-%d %H:%M:%S')],
            '0-20-can_attend': ['True'], '0-20-starttime': [cls.time_list[20].strftime('%Y-%m-%d %H:%M:%S')],
            '0-21-can_attend': ['True'], '0-21-starttime': [cls.time_list[21].strftime('%Y-%m-%d %H:%M:%S')],
            '0-22-can_attend': ['True'], '0-22-starttime': [cls.time_list[22].strftime('%Y-%m-%d %H:%M:%S')],
            '0-23-can_attend': ['True'], '0-23-starttime': [cls.time_list[23].strftime('%Y-%m-%d %H:%M:%S')],
            '0-24-can_attend': ['True'], '0-24-starttime': [cls.time_list[24].strftime('%Y-%m-%d %H:%M:%S')],
            '0-25-can_attend': ['True'], '0-25-starttime': [cls.time_list[25].strftime('%Y-%m-%d %H:%M:%S')],
            '0-26-can_attend': ['True'], '0-26-starttime': [cls.time_list[26].strftime('%Y-%m-%d %H:%M:%S')],
            '0-27-can_attend': ['True'], '0-27-starttime': [cls.time_list[27].strftime('%Y-%m-%d %H:%M:%S')],
            '0-28-can_attend': ['True'], '0-28-starttime': [cls.time_list[28].strftime('%Y-%m-%d %H:%M:%S')],
            '0-29-can_attend': ['True'], '0-29-starttime': [cls.time_list[29].strftime('%Y-%m-%d %H:%M:%S')],
            '0-30-can_attend': ['True'], '0-30-starttime': [cls.time_list[30].strftime('%Y-%m-%d %H:%M:%S')],
            '0-31-can_attend': ['True'], '0-31-starttime': [cls.time_list[31].strftime('%Y-%m-%d %H:%M:%S')],
            '0-32-can_attend': ['True'], '0-32-starttime': [cls.time_list[32].strftime('%Y-%m-%d %H:%M:%S')],
            '0-33-can_attend': ['True'], '0-33-starttime': [cls.time_list[33].strftime('%Y-%m-%d %H:%M:%S')],
            }

    def test_input_calendar_POST_logOUT(self):
        User_LogOUT(self)
        request = self.client.post(self.url, self.data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_input_calendar_POST_logIN(self):
        user = Force_Login(self)
        request = self.client.post(self.url, self.data)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, '/awase/calendar/%s/' % str(self.calendar.pk))
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/calendar.html')
        
        for time in self.time_list:
            self.assertTrue(Schedule.objects.filter(
                calendar = self.calendar,
                user = user,
                start_time = time,
                can_attend = True,
                ).exists())
            self.assertFalse(Schedule.objects.filter(
                calendar = self.calendar,
                user = user,
                start_time = time,
                can_attend = False,
                ).exists())


class CalendarInvitionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Make_User(self)
        self.calendar = Make_a_Calendar(self)
        self.url = '/awase/invited/key=%s/' % self.calendar.invite_key

    def test_calendar_invite_logOUT(self):
        logOUT_test_view(self, self.url)

    def test_calendar_invite_logIN(self):
        newuser = Make_User(self, year=2018)
        self.assertFalse(CalendarUser.objects.filter(calendar=self.calendar, user=newuser).exists())
        
        Force_Login(self, year=2018)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/invited.html')
        self.assertFalse(CalendarUser.objects.filter(calendar=self.calendar, user=newuser).exists())
        
        request = self.client.post(self.url, {'join': ['true']})
        self.assertTrue(CalendarUser.objects.filter(calendar=self.calendar, user=newuser).exists())
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'awase/calendar.html')
        

class UpdateCollectHourTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Make_User(self)
        self.calendar = Make_a_Calendar(self)
        self.url = '/awase/update/hours/%s/' % self.calendar.pk

    def test_calendar_update_collecthour_logOUT(self):
        logOUT_test_view(self, self.url)

    # def test_calendar_update_collecthour_logIN_POST(self):
    #     instance = CollectHour.objects.get(
    #         calendar = self.calendar,
    #         date = self.calendar.days_begin,
    #         )
    #     data = {
    #         'form-0-hour_begin': ['9'],
    #         'form-0-hour_end': ['26'],
    #         'form-0-date': [str(instance.date.strftime('%Y-%m-%d'))],
    #         'form-0-id': [str(instance.id)],
    #     }
        # formset = UpdateCollectHourFormSet(data)
        # self.assertTrue(formset.is_valid())
        
        # Force_Login(self)
        # request = self.client.post(self.url, data)
        # self.assertEqual(request.status_code, 302)
        # url_redial_to = request.url
        # response = self.client.get(url_redial_to)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'awase/calendar.html')
