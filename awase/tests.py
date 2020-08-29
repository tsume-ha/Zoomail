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
        url = '/awase/%s/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/calendar.html')

    def test_awase_input_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/input/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_input_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/input/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/input.html')

    def test_awase_update_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/update/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/update/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_calendar.html')

    def test_awase_update_hours_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/hours/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_hours_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/hours/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_hours.html')

    def test_awase_update_urlkey_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/urlkey/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_urlkey_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/urlkey/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/update_URLKey.html')

    def test_awase_update_user_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/user/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_update_user_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/user/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/change_users.html')

    def test_awase_leave_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/leave/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_leave_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/leave/' % str(calendar.pk)
        response = logIN_test_view(self, calendar=calendar, url=url)
        self.assertTemplateUsed(response, 'awase/leave_calendar.html')

    def test_awase_delete_calendar_view_logOUT(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/delete/' % str(calendar.pk)
        logOUT_test_view(self, url=url)

    def test_awase_delete_calendar_view_logIN(self):
        calendar = Make_a_Calendar(self)
        url = '/awase/%s/delete/' % str(calendar.pk)
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
            'days_begin': ['2020-04-01'],
            'days_end': ['2020-04-10'],
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
            'days_begin': ['2020-04-01'],
            'days_end': ['2020-04-20'],
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
            date = datetime.datetime.strptime(data['days_begin'][0], '%Y-%m-%d') - datetime.timedelta(days=1)
            ).exists())
        self.assertTrue(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.datetime.strptime(data['days_begin'][0], '%Y-%m-%d')
            ).exists())
        self.assertTrue(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.datetime.strptime(data['days_end'][0], '%Y-%m-%d')
            ).exists())
        self.assertFalse(CollectHour.objects.filter(
            calendar = calendar,
            date = datetime.datetime.strptime(data['days_end'][0], '%Y-%m-%d') + datetime.timedelta(days=1)
            ).exists())


class CalendarInputTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)
        cls.calendar = Make_a_Calendar(cls)
        cls.url = '/awase/%s/input/' % str(cls.calendar.pk)
        cls.time_list = [datetime.datetime.combine(datetime.date.today(), datetime.time(00,00,00))\
                      + datetime.timedelta(days=1, hours=9)\
                      + datetime.timedelta(minutes=30*n)
                     for n in range((26-9)*2)]
        cls.data = {}
        
        # viewからコピーしてきた
        def getOver24h(dt):  # Datetime => String
            if 0 <= dt.hour <= 5:
                t = 12  # 適当な時間をさかのぼって、そこからの経過時間を計算する
                tmp = dt - datetime.timedelta(hours=t)
                hour = tmp.hour + 12  # ここで二ケタの保証はされるから、0埋めはしない
                return tmp.strftime('%Y%m%d_') + str(hour) + tmp.strftime('%M')
            else:
                return dt.strftime('%Y%m%d_%H%M')

        for time in cls.time_list:
            YYYYMMDD_HHMM = getOver24h(time)
            cls.data[YYYYMMDD_HHMM] = 'true'

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
        request = self.client.post(
            '/awase/%s/input/json/' % str(self.calendar.pk), self.data,
            content_type='application/json'#json送るときこれ必要
            )
        self.assertEqual(request.status_code, 200)
        #自動送信なので自分で遷移する（下行）
        response = self.client.get('/awase/%s/' % str(self.calendar.pk))
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
        self.url = '/awase/%s/hours/' % self.calendar.pk

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
