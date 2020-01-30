from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
from .forms import CreateCalendarForm, InputScheduleForm
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory
from django.db.models import Count
from django.http import Http404
from django.http.response import JsonResponse
from django.urls import reverse

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
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    params = {
        'timetuple': list(range(9,26)),
        'calendar': calendar,
    }
    return render(request, 'awase/calendar.html', params)

@login_required()
def CalendarJsonResponse(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    
    LIMIT_DAYS = 100
    today = datetime.date.today()
    if (calendar.days_end - calendar.days_begin).days > LIMIT_DAYS:
        if calendar.days_begin <= today < calendar.days_end:
            collect_days = [today + datetime.timedelta(days=d) for d in range(LIMIT_DAYS)]
        elif today < calendar.days_begin:
            collect_days = [calendar.days_begin + datetime.timedelta(days=d) for d in range(LIMIT_DAYS)]
        else: # calendar.days_end <= today
            collect_days = [calendar.days_end - datetime.timedelta(days=LIMIT_DAYS) + datetime.timedelta(days=d) for d in range(LIMIT_DAYS)]
    else:
        collect_days = [calendar.days_begin + datetime.timedelta(days=d) for d in range((calendar.days_end - calendar.days_begin).days + 1)]
    
    data = {
        'calendar_data': [],
        'settings': {
            'total_days': (calendar.days_end - calendar.days_begin).days,
            'today_num': (today - calendar.days_begin).days,
        }
    }

    weekday_jp = ['月','火','水','木','金','土','日']
    NG_CSS_classname = ['NG0', 'NG1', 'NG2', 'NG3']
    for day in collect_days:
        day_json = {
            'date': day.strftime('%Y-%m-%d'),
            'display_date': f"{day.month}/{day.day}",
            'display_day': weekday_jp[day.weekday()],
            'room': 'Loading',
            'NGlist':{}
        }
        hours = CollectHour.objects.filter(calendar=calendar).get(date=day)
        timelist = [
            datetime.datetime.combine(day, datetime.time(0)) + datetime.timedelta(minutes=30*h)
            for h in range(hours.hour_begin*2,hours.hour_end*2)
            ]
        for time in timelist:
            if time.hour > 5:
                time_label = time.strftime('%H_%M')
            else:
                time_label = str(time.hour + 24) + '_' + str(time.minute)
            
            is_answered = Schedule.objects.filter(calendar=calendar, starttime=time).exists()
            if not is_answered:
                day_json['NGlist'][time_label] = ''
                continue
            num = Schedule.objects.filter(calendar=calendar, starttime=time, canattend=False).aggregate(Count('starttime'))['starttime__count']
            if num < 4:
                day_json['NGlist'][time_label] = NG_CSS_classname[num]
            else:
                day_json['NGlist'][time_label] = NG_CSS_classname[3]
        data['calendar_data'].append(day_json)

    return JsonResponse(data)


@login_required()
def create(request):
    now_user = request.user
    CreateForm = CreateCalendarForm(request.POST or None)
    if (request.method == 'POST'):
        if CreateForm.is_valid():
            content = CreateForm.save(commit=False)
            try:
                calendar = Calendar.objects.get(title=content.title, text=content.text, days_begin=content.days_begin, days_end=content.days_end)
            except ObjectDoesNotExist:
                content.created_by = now_user
                content.invite_key = User.objects.make_random_password(length=12)
                content.save()
                calendar = content
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
                user_content = CalendarUser(
                    calendar = content,
                    user = now_user
                    )
                user_content.save()
            params ={'calendar': calendar}
            return render(request, 'awase/create_complete.html', params)
        else:
            print('Form is not valid')
    params = {
        'CreateForm': CreateForm,

    }

    return render(request, 'awase/create.html', params)

@login_required()
def invited(request, key):
    now_user = request.user
    calendar = Calendar.objects.get(invite_key=key)
    if CalendarUser.objects.filter(calendar=calendar, user=now_user).exists():
        messages.warning(request, calendar.title + 'にはすでに参加しています。')
        return redirect(to = reverse('awase:calendar', args=[calendar.pk]))
    if (request.method == 'POST'):
        if request.POST['join'] == 'true':
            user_content = CalendarUser(
                calendar = calendar,
                user = now_user
                )
            user_content.save()
            messages.success(request, calendar.title + 'に参加しました。')
            return redirect(to = reverse('awase:calendar', args=[calendar.pk]))
    params = {
        'calendar': calendar,
    }
    return render(request, 'awase/invited.html', params)


@login_required()
def input(request, pk, page=1):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    can_edit = calendar_permission(calendar, now_user)
    if can_edit:
        if (request.method == 'POST'):
            print(request.POST)
            keys = [k for k in request.POST if 'can_attend' in k]
            for key in keys:
                time_name = key.replace('can_attend', 'datetime')
                time = request.POST[time_name]
                can_attend = request.POST[key]
                Schedule.objects.update_or_create(
                    calendar = calendar,
                    user = now_user,
                    starttime = time,
                    defaults = {'canattend': can_attend}
                )
            return redirect(to='../')

        formsets = []
        InputScheduleFormSet = formset_factory(InputScheduleForm, extra=0)
        schedule_calendar_query = Schedule.objects.filter(calendar=calendar).filter(user=now_user)
        date = calendar.days_begin + datetime.timedelta(days=7*(page-1))
        date_range = {'start': date}
        count = 0
        while date <= calendar.days_end and date < calendar.days_begin + datetime.timedelta(days=7*page):
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
            date_range['end'] = date
            date = date + datetime.timedelta(days=1)
        import math
        total_pages = math.ceil((calendar.days_end - calendar.days_begin).days / 7)
        params = {
            'calendar': calendar,
            'formsets': formsets,
            'prev': page-1,
            'page': page,
            'next': page+1,
            'total_pages': total_pages,
            'date_range': date_range,
        }


        return render(request, 'awase/input.html', params)
    else:
        return redirect('/awase/')