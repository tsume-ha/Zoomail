from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from .models import Calendar, CalendarUser, Schedule


@login_required()
def index(request):
    now_user = request.user
    calendar_query = Calendar.objects.filter(calendar_content__user=now_user).order_by('created_at').reverse()
    params = {
        'calendars': calendar_query,
    }
    return render(request, 'awase/index.html', params)

@login_required()
def calendar(request, pk):
    display_date = (
        datetime.date(2019,10,10),
        datetime.date(2019,10,11),
        datetime.date(2019,10,12),
        datetime.date(2019,10,13),
        datetime.date(2019,10,14),
        datetime.date(2019,10,15),
        datetime.date(2019,10,16),
        )
    NG_0_list = [
        {'date' : datetime.date(2019,10,10), 'time' : 14, 'half' : False},
        {'date' : datetime.date(2019,10,11), 'time' : 14, 'half' : False},
        {'date' : datetime.date(2019,10,12), 'time' : 14, 'half' : False},
        {'date' : datetime.date(2019,10,13), 'time' : 14, 'half' : False},
        {'date' : datetime.date(2019,10,14), 'time' : 14, 'half' : True},
        {'date' : datetime.date(2019,10,15), 'time' : 14, 'half' : True},
        {'date' : datetime.date(2019,10,16), 'time' : 14, 'half' : True},
    ]
    NG_1_list = [
        {'date' : datetime.date(2019,10,10), 'time' : 15, 'half' : False},
        {'date' : datetime.date(2019,10,13), 'time' : 15, 'half' : True},
        {'date' : datetime.date(2019,10,14), 'time' : 15, 'half' : True},
        {'date' : datetime.date(2019,10,15), 'time' : 15, 'half' : True},
        {'date' : datetime.date(2019,10,16), 'time' : 15, 'half' : True},
    ]
    NG_2_list = [
        {'date' : datetime.date(2019,10,10), 'time' : 18, 'half' : False},
        {'date' : datetime.date(2019,10,11), 'time' : 18, 'half' : False},
        {'date' : datetime.date(2019,10,12), 'time' : 18, 'half' : False},
        {'date' : datetime.date(2019,10,13), 'time' : 18, 'half' : False},
        {'date' : datetime.date(2019,10,14), 'time' : 18, 'half' : False},
        {'date' : datetime.date(2019,10,14), 'time' : 18, 'half' : True},
        {'date' : datetime.date(2019,10,15), 'time' : 18, 'half' : True},
        {'date' : datetime.date(2019,10,16), 'time' : 18, 'half' : True},
    ]
    NG_3over_list = [
        {'date' : datetime.date(2019,10,10), 'time' : 20, 'half' : False},
        {'date' : datetime.date(2019,10,11), 'time' : 20, 'half' : False},
        {'date' : datetime.date(2019,10,12), 'time' : 20, 'half' : False},
        {'date' : datetime.date(2019,10,13), 'time' : 20, 'half' : False},
        {'date' : datetime.date(2019,10,14), 'time' : 20, 'half' : False},
    ]
    params = {
        'timetuple': (n for n in range(9,27)),
        'datetuple': display_date,
        'NG_0_list' : NG_0_list,
        'NG_1_list' : NG_1_list,
        'NG_2_list' : NG_2_list,
        'NG_3over_list' : NG_3over_list,
    }
    return render(request, 'awase/calendar.html', params)


@login_required()
def create(request):

    params = {

    }

    return render(request, 'awase/create.html', params)

@login_required()
def input(request, pk):

    params = {
    
    }

    return render(request, 'awase/create.html', params)