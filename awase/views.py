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
from django.db.models import Count
from django.http import Http404
from django.http.response import JsonResponse

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
def CalendarView(request, pk):
    now_user = request.user
    calendar = Calendar.objects.get(pk=pk)
    pagenum = 0
    if (calendar.days_end - calendar.days_begin).days < 7:
        displaydays = (calendar.days_end - calendar.days_begin).days + 1
    else:
        displaydays = 7
    display_date = [calendar.days_begin + datetime.timedelta(days=d+pagenum*7) for d in range(displaydays)]
    NG = [
        [],#0
        [],#1
        [],#2
        [],#over3
        ]
    for day in display_date:
        hours = CollectHour.objects.filter(calendar=calendar).get(date=day)
        timelist = [datetime.datetime.combine(day, datetime.time(0)) + datetime.timedelta(minutes=30*h)
                    for h in range(hours.hour_begin*2,hours.hour_end*2)]
        for time in timelist:
            is_answered = Schedule.objects.filter(calendar=calendar, starttime=time).exists()
            if not is_answered:
                continue
            num = Schedule.objects.filter(calendar=calendar, starttime=time, canattend=False)\
                .aggregate(Count('starttime'))['starttime__count']
            data = {'date' : day}
            if 0 <= time.hour <= 5:
                data['time'] = time.hour + 24
            else:
                data['time'] = time.hour
            if time.minute == 0:
                data['half'] = False
            else:
                data['half'] = True
            if num < 4:
                NG[num].append(data)
            else:
                NG[3].append(data)
    params = {
        'timetuple': (n for n in range(9,26)),
        'datetuple': display_date,
        'NG_0_list' : NG[0],
        'NG_1_list' : NG[1],
        'NG_2_list' : NG[2],
        'NG_3over_list' : NG[3],
    }
    return render(request, 'awase/calendar.html', params)

@login_required()
def CalendarJsonResponse(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    data = {
        '2019-12-12': {'9:00': 3, '9:30': 3, '10:00': 3, '10:30': 3, '11:00': 3, '11:30': 3, '12:00': 3, '12:30': 3, '13:00': 3,},
        '2019-12-13': {'9:00': 3, '9:30': 3, '10:00': 3, '10:30': 3, '11:00': 3, '11:30': 3, '12:00': 3, '12:30': 3, '13:00': 3,},
        '2019-12-14': {'9:00': 3, '9:30': 3, '10:00': 3, '10:30': 3, '11:00': 3, '11:30': 3, '12:00': 3, '12:30': 3, '13:00': 3,},
        }
    return JsonResponse(data)


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
        if (request.method == 'POST'):
            keys = [k for k in request.POST if 'can_attend' in k]
            for key in keys:
                time_name = key.replace('can_attend', 'datetime')
                time = request.POST[time_name]
                can_attend = request.POST[key]
                Schedule.objects.update_or_create(
                    calendar = calendar,
                    user = now_user,
                    starttime = time,
                    defaults = {'duration': 30, 'canattend': can_attend}
                )
            return redirect(to='../')

        formsets = []
        InputScheduleFormSet = formset_factory(InputScheduleForm, extra=0)
        schedule_calendar_query = Schedule.objects.filter(calendar=calendar).filter(user=now_user)
        date = calendar.days_begin
        count = 0
        while date <= calendar.days_end:
            hour_query = CollectHour.objects.filter(calendar=calendar).get(date=date)
            initial_data = []
            for t in range(hour_query.hour_begin, hour_query.hour_end):
                datetime_data = datetime.datetime.combine(date, datetime.time(00,00,00))
                datetime_data = datetime_data + datetime.timedelta(hours=t)
                try:
                    schedule_query = schedule_calendar_query.get(starttime=datetime_data)
                    initial_data.append({
                        'displaytime':datetime_data.strftime('%H:%M'),
                        'datetime':datetime_data,
                        'can_attend': schedule_query.canattend
                        })
                except ObjectDoesNotExist:
                    initial_data.append({
                        'displaytime':datetime_data.strftime('%H:%M'),
                        'datetime':datetime_data
                        })
                datetime_data = datetime_data + datetime.timedelta(minutes=30)
                try:
                    schedule_query = schedule_calendar_query.get(starttime=datetime_data)
                    initial_data.append({
                        'displaytime':datetime_data.strftime('%H:%M'),
                        'datetime':datetime_data,
                        'can_attend': schedule_query.canattend
                        })
                except ObjectDoesNotExist:
                    initial_data.append({
                        'displaytime':datetime_data.strftime('%H:%M'),
                        'datetime':datetime_data
                        })
            formsets.append({'date':date, 'InputScheduleFormSet':InputScheduleFormSet(initial=initial_data,prefix=str(count))})
            count += 1
            date = date + datetime.timedelta(days=1)
        params = {
            'calendar': calendar,
            'formsets': formsets,
        }


        return render(request, 'awase/input.html', params)
    else:
        return redirect('/awase/')