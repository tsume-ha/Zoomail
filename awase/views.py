from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
from .forms import CreateCalendarForm, InviteUserForm, InputScheduleForm
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory

def calendar_permission(calendar, user):
    return CalendarUser.objects.filter(calendar=calendar).filter(user=user).exists()

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
    now_user = request.user
    CreateForm = CreateCalendarForm(request.POST or None)
    InviteForm = InviteUserForm(request.POST or None)
    if (request.method == 'POST'):
        if CreateForm.is_valid():
            try:
                inviteduser = request.POST['user_post_data']
            except MultiValueDictKeyError:
                pass
            if inviteduser != '':
                content = CreateForm.save(commit=False)
                content.created_by = now_user
                content.save()
                print(inviteduser)
                inviteduser_list = inviteduser.split(',')
                print(inviteduser_list)
                for user_pk in inviteduser_list:
                    try:
                        user = User.objects.get(pk=int(user_pk[5]))
                    except ObjectDoesNotExist:
                        continue
                    calendar_user_content = CalendarUser(
                        calendar = content,
                        user = user
                        )
                    calendar_user_content.save()
                date = content.days_begin
                while date <= content.days_end:
                    date_content = CollectHour(
                        calendar=content,
                        date=date,
                        hour_begin=9,
                        hour_end=26,
                        )
                    date_content.save()
                    date = date + datetime.timedelta(days=1)
                return redirect(to='../')

        else:
            print('Form is not valid')
    years = User.objects.order_by().values('year').distinct()
    InviteForm.fields['year_choice'].choices = [(q['year'],q['year']) for q in years]
    InviteForm.fields['invite_user'].choices = [(str(user.year).zfill(4)+'_'+str(user.pk), user.get_short_name) for user in User.objects.all().order_by('year').order_by('furigana')]

    params = {
        'CreateForm': CreateForm,
        'InviteForm': InviteForm,

    }

    return render(request, 'awase/create.html', params)

@login_required()
def input(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    can_edit = calendar_permission(calendar, now_user)
    if can_edit:
        # initial_data = [
        #     {'can_attend': True, 'datetime': datetime.datetime(2019,10,19,22,00,00)},
        #     {'can_attend': True, 'datetime': datetime.datetime(2019,10,19,23,00,00)}
        #     ]
        # InputScheduleFormSet = formset_factory(InputScheduleForm, extra=0)
        # formset = [InputScheduleFormSet(initial=initial_data), InputScheduleFormSet(initial=initial_data)]
        formsets = []
        schedule_calendar_query = Schedule.objects.filter(calendar=calendar).filter(user=now_user)
        date = calendar.days_begin
        while date <= calendar.days_end:
            hour_query = CollectHour.objects.filter(calendar=calendar).get(date=date)
            initial_data = []
            for t in range(hour_query.hour_begin, hour_query.hour_end):
                try:
                    schedule_query = schedule_calendar_query.get(starttime=datetime.datetime(date.year,date.month,date.day,t,00,00))
                    print(schedule_query)
                except ObjectDoesNotExist:
                    pass
                
            date = date + datetime.timedelta(days=1)
        params = {
            'calendar': calendar,
            'formset': formset,
        }

        return render(request, 'awase/input.html', params)
    else:
        return redirect('/awase/')