from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
import json
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
from .forms import CreateCalendarForm, InputScheduleFormSet, UpdateCollectHourFormSet, UserChangeFormSet, UpdateCollectHourForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.http.response import JsonResponse
from django.urls import reverse

def calendar_permission(calendar, user):
    return CalendarUser.objects.filter(calendar=calendar).filter(user=user).exists()

def ceil(a, b):
    return a//b if a%b==0 else a//b + 1

CALENDAR_MAX_RANGE = 120 # max days

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
 
    data = {
        'calendar_data': [],
        'settings': {
            'total_days': (calendar.days_end - calendar.days_begin).days + 1,
            'today_num': (datetime.date.today() - calendar.days_begin).days,
        }
    }

    weekday_jp = ['月','火','水','木','金','土','日']

    user_list = CalendarUser.objects.filter(calendar=calendar).order_by('joined_at')


    def get_time_str(day, time):
        hour = time.hour + (time - datetime.datetime.combine(day, datetime.time(00,00,00))).days * 24
        return 't' + str(hour) + '_' + str(time.minute)

    for day in [calendar.days_begin + datetime.timedelta(days=d) for d in range((calendar.days_end - calendar.days_begin).days + 1)]:
        schedule_list = {}
        complex_list = []
        hour_begin = CollectHour.objects.get(calendar=calendar, date=day).hour_begin
        hour_end = CollectHour.objects.get(calendar=calendar, date=day).hour_end

        for calendar_user in user_list:
            tmp = Schedule.objects.filter(
                calendar = calendar,
                user = calendar_user.user,
                start_time__gte = datetime.datetime.combine(day, datetime.time(hour=hour_begin)),
                start_time__lt = datetime.datetime.combine(day, datetime.time(hour=hour_end%24)) + datetime.timedelta(days=hour_end//24)
                ).values_list('start_time', 'can_attend')
            tmp_dict = {}
            for starttime, canattend in tmp:
                tmp_dict[get_time_str(day, starttime)] = canattend
            if calendar_user.user.nickname == "":
                schedule_list[calendar_user.user.get_full_name()] = tmp_dict
            else:
                schedule_list[calendar_user.user.get_short_name() + '(' + calendar_user.user.get_full_name() + ')'] = tmp_dict

        day_json = {
            'date': day.strftime('%Y-%m-%d'),
            'display_date': str(day.month) + '/' + str(day.day),
            'display_day': weekday_jp[day.weekday()],
            'weekday': day.weekday(),
            'hour_begin': hour_begin,
            'hour_end': hour_end,
            'schedule_list':schedule_list,
            'room': 'Loading',
        }
        data['calendar_data'].append(day_json)

    return JsonResponse(data)


@login_required()
def create(request):
    now_user = request.user
    CreateForm = CreateCalendarForm(request.POST or None)
    if (request.method == 'POST'):
        if not CreateForm.is_valid():
            messages.error(request, '登録できませんでした。もう一度入力を行ってください。')
        else:
            content = CreateForm.save(commit=False)
            content.created_by = now_user
            content.invite_key = User.objects.make_random_password(length=12)
            content.save()
            calendar = content
            user_content = CalendarUser(
                calendar = content,
                user = now_user
                )
            user_content.save()
            params ={'calendar': calendar}
            return render(request, 'awase/create_complete.html', params)

    params = {
        'CreateForm': CreateForm,
    }

    return render(request, 'awase/create.html', params)

@login_required()
def invited(request, key):
    now_user = request.user
    calendar = get_object_or_404(Calendar, invite_key=key)
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
def input(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()

    params = {
        'calendar': calendar,
    }


    return render(request, 'awase/input.html', params)


@login_required()
def inputJSON(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    
    if (request.method == 'POST' and request.body):
        json_dict = json.loads(request.body)

        def getDatetime(key):# String, YYYYMMDD_HHMM => Datetime
            dt = datetime.datetime(year=int(key[0:4]), month=int(key[4:6]), day=int(key[6:8]))
            dt += datetime.timedelta(hours=int(key[9:11]), minutes=int(key[11:13]))
            return dt
            
        for key in json_dict:
            try:
                Schedule.objects.update_or_create(
                    calendar=calendar,
                    user=now_user,
                    start_time=getDatetime(key),
                    defaults={
                        'can_attend': bool(json_dict[key])
                    }
                )
            except:
                response = HttpResponse('BAD REQUEST')
                response.status_code = 400
                return response

        response = HttpResponse('OK')
        response.status_code = 200
        return response


    def getOver24h(dt):# Datetime => String
        if 0 <= dt.hour <= 5:
            t = 12# 適当な時間をさかのぼって、そこからの経過時間を計算する
            tmp = dt - datetime.timedelta(hours=t)
            hour = tmp.hour + 12# ここで二ケタの保証はされるから、0埋めはしない
            return tmp.strftime('%Y%m%d_') + str(hour) + tmp.strftime('%M')
        else:
            return dt.strftime('%Y%m%d_%H%M')

    data = {}
    RangeDataList = CollectHour.objects.filter(
        calendar=calendar, date__gte=calendar.days_begin, date__lte=calendar.days_end
        ).order_by('date').values_list('date', 'hour_begin', 'hour_end')
    data['HourRange'] = {RangeData[0].strftime('%Y%m%d'): {'start': RangeData[1], 'end': RangeData[2]} for RangeData in RangeDataList}
    ScheduleDataList = Schedule.objects.filter(user=now_user, calendar=calendar).values_list('start_time', 'can_attend')
    data['Schedule'] = {getOver24h(ScheduleData[0]): ScheduleData[1] for ScheduleData in ScheduleDataList}

    if datetime.date.today() <= calendar.days_begin:
        data['InitialDate'] = calendar.days_begin.strftime('%Y%m%d')
    elif calendar.days_begin < datetime.date.today() <= calendar.days_end:
        data['InitialDate'] = datetime.date.today().strftime('%Y%m%d')
    else:
        data['InitialDate'] = calendar.days_end.strftime('%Y%m%d')

    return JsonResponse(data)


@login_required()
def UpdateCalendarView(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    UpdateForm = CreateCalendarForm(request.POST or None, instance=calendar)
    if (request.method == 'POST'):
        if UpdateForm.is_valid():
            content = UpdateForm.save()
            return redirect(to=reverse('awase:calendar', args=[calendar.pk]))
            

    params = {
        'calendar': calendar,
        'UpdateForm': UpdateForm,

    }

    return render(request, 'awase/update_calendar.html', params)



@login_required()
def UpdateCollectHourView(request, pk, page=1):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    DISPLAY_DAYS = 30
    updateFormset = UpdateCollectHourFormSet(
        request.POST or None,
        queryset=CollectHour.objects.filter(
            calendar = calendar,
            date__gte = calendar.days_begin,
            date__lte = calendar.days_end
            ).order_by('date')[(page - 1) * DISPLAY_DAYS : page * DISPLAY_DAYS],
        form_kwargs={'empty_permitted': False}
    )
    if (request.method == 'POST'):
        if updateFormset.is_valid():
            content = updateFormset.save()
            return redirect(to=reverse('awase:calendar', args=[calendar.pk]))

    total_pages = ceil((calendar.days_end - calendar.days_begin).days + 1, DISPLAY_DAYS)
    page_range = list(range(1, total_pages + 1))

    params = {
        'calendar': calendar,
        'updateFormset': updateFormset,
        'page_range': page_range,
        'total_pages': total_pages,
        'current_page': page,

    }

    return render(request, 'awase/update_hours.html', params)

@login_required()
def CollectHourJsonResponse(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()

    if (request.method == 'POST' and request.body):
        json_dict = json.loads(request.body)
        is_error = False;
        for (YYYYMMDD, time_range) in json_dict.items():
            date = datetime.date(
                year = int(YYYYMMDD[0:4]),
                month = int(YYYYMMDD[4:6]),
                day = int(YYYYMMDD[6:8])
                )
            time_list = time_range.split('-')
            start = time_list[0]
            end = time_list[1]

            instance = CollectHour.objects.get(calendar=calendar, date=date)

            form = UpdateCollectHourForm({
                'date': date,
                'hour_begin': start,
                'hour_end': end
                }, instance = instance)
            if form.is_valid():
                form.save()
            else:
                is_error = True
        if is_error:
            response = HttpResponse('BAD REQUEST')
            response.status_code = 400
            return response
        else:
            response = HttpResponse('OK')
            response.status_code = 200
            return response


    datalist = CollectHour.objects.filter(calendar=calendar).order_by('date').values_list('date', 'hour_begin', 'hour_end')
    data = {data[0].strftime('%Y%m%d'): {'start': data[1], 'end': data[2]} for data in datalist}

    return JsonResponse(data)



@login_required()
def CalendarURLKey(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    params = {
        'calendar': calendar,
    }
    return render(request, 'awase/update_URLKey.html', params)

@login_required()
def ChangeUsers(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    
    formset = UserChangeFormSet(request.POST or None, queryset=CalendarUser.objects.filter(
        calendar = calendar
        ))
    if (request.method == 'POST'):
        if formset.is_valid():
            formset.save()
            messages.success(request, 'メンバーを退会させました。')
            return redirect(to=reverse('awase:calendar', args=[calendar.pk]))
    params = {
        'calendar': calendar,
        'formset': formset,
    }
    return render(request, 'awase/change_users.html', params)


@login_required()
def LeaveCalendarView(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    if (request.method == 'POST'):
        if 'leave' in request.POST:
            content = CalendarUser.objects.filter(calendar=calendar, user=now_user)
            content.delete()
            messages.success(request, calendar.title + 'から退会しました。')
            return redirect(to=reverse('awase:index'))

    params = {
        'calendar': calendar,
    }
    return render(request, 'awase/leave_calendar.html', params)


@login_required()
def DeleteCalendarView(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    if (request.method == 'POST'):
        if 'delete' in request.POST:
            calendar.delete()
            messages.success(request, calendar.title + 'を削除しました。')
            return redirect(to=reverse('awase:index'))

    params = {
        'calendar': calendar,
    }
    return render(request, 'awase/delete_calendar.html', params)



