from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from members.models import User
from .models import Calendar, CalendarUser, Schedule, CollectHour
from .forms import CreateCalendarForm, InputScheduleFormSet, UpdateCollectHourFormSet, UserChangeFormSet
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
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

    user_list = CalendarUser.objects.filter(calendar=calendar).order_by('joined_at')


    def get_time_str(day, time):
        hour = time.hour + (time - datetime.datetime.combine(day, datetime.time(00,00,00))).days * 24
        return 't' + str(hour) + '_' + str(time.minute)

    for day in collect_days:
        schedule_list = {}
        complex_list = []
        hour_begin = CollectHour.objects.get(calendar=calendar, date=day).hour_begin
        hour_end = CollectHour.objects.get(calendar=calendar, date=day).hour_end

        for calendar_user in user_list:
            tmp = Schedule.objects.filter(
                calendar = calendar,
                user = calendar_user.user,
                starttime__gte = datetime.datetime.combine(day, datetime.time(hour=hour_begin)),
                starttime__lt = datetime.datetime.combine(day, datetime.time(hour=hour_end%24)) + datetime.timedelta(days=hour_end//24)
                ).values_list('starttime', 'canattend')
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
    if not calendar_permission(calendar, now_user):
        raise Http404()
        
    def ceil(a, b):
        return a//b if a%b==0 else a//b + 1
    total_pages = ceil((calendar.days_end - calendar.days_begin).days, 7)

    move = False
    if 'prev' in request.GET:
        page -= 1
        move = True
        if page < 0:
            page = 1

    if 'next' in request.GET:
        page += 1
        move = True
        if page > total_pages:
            page = total_pages

    if (request.method == 'POST'):
        keys = [k for k in request.POST if 'can_attend' in k]
        for key in keys:
            time_name = key.replace('can_attend', 'starttime')
            time = request.POST[time_name]
            can_attend = request.POST[key]
            Schedule.objects.update_or_create(
                calendar = calendar,
                user = now_user,
                starttime = time,
                defaults = {'canattend': can_attend}
            )
        if move:
            return redirect(to = reverse('awase:input', args=[calendar.pk, page]))
        else:
            return redirect(to = reverse('awase:calendar', args=[calendar.pk]))


    formsets = []

    date = calendar.days_begin + datetime.timedelta(days=7*(page-1))
    count = 0
    date_range = {'start': date}
    while date <= calendar.days_end and date < calendar.days_begin + datetime.timedelta(days=7*page):
        hour_query = CollectHour.objects.filter(calendar=calendar).get(date=date)
        time_list = [datetime.datetime.combine(date, datetime.time(00,00,00))\
                      + datetime.timedelta(hours=hour_query.hour_begin)\
                      + datetime.timedelta(minutes=30*n)
                     for n in range((hour_query.hour_end-hour_query.hour_begin)*2)]
        if len(time_list):
            initial = []
            for time in time_list:
                item, created = Schedule.objects.get_or_create(
                    calendar = calendar,
                    user = now_user,
                    starttime = time,
                    defaults = {'canattend': ''}
                    )
                initial.append({
                    'displaytime':time.strftime('%H:%M'),
                    'starttime':time,
                    'can_attend': item.canattend
                    })

            formsets.append({
                'date':date,
                'InputScheduleFormSet':InputScheduleFormSet(
                    initial = initial,
                    prefix = str(count)
                    )
                })
        count += 1
        date = date + datetime.timedelta(days=1)
    date_range['end'] = date - datetime.timedelta(days=1)

    params = {
        'calendar': calendar,
        'formsets': formsets,
        'page': page,
        'date_range': date_range,
        'total_pages': total_pages,
    }


    return render(request, 'awase/input.html', params)


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

            date = content.days_begin
            while date <= content.days_end:
                date_content = CollectHour.objects.get_or_create(
                    calendar = calendar,
                    date = date,
                    defaults = {'hour_begin': 9, 'hour_end': 26},
                    )
                date = date + datetime.timedelta(days=1)

            return redirect(to=reverse('awase:calendar', args=[calendar.pk]))
        else:
            print('form is not valid')

    params = {
        'calendar': calendar,
        'UpdateForm': UpdateForm,

    }

    return render(request, 'awase/update_calendar.html', params)



@login_required()
def UpdateCollectHourView(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    updateFormset = UpdateCollectHourFormSet(request.POST or None, queryset=CollectHour.objects.filter(
        calendar = calendar,
        date__gte = calendar.days_begin,
        date__lte = calendar.days_end
        ).order_by('date')
    )
    if (request.method == 'POST'):
        if updateFormset.is_valid():
            content = updateFormset.save()
            return redirect(to=reverse('awase:calendar', args=[calendar.pk]))
        else:
            print('validationerror')
    params = {
        'calendar': calendar,
        'updateFormset': updateFormset,

    }

    return render(request, 'awase/update_hours.html', params)


@login_required()
def UpdateURLKey(request, pk):
    now_user = request.user
    calendar = get_object_or_404(Calendar, pk=pk)
    if not calendar_permission(calendar, now_user):
        raise Http404()
    if (request.method == 'POST'):
        if 'change_key' in request.POST:
            calendar.invite_key = User.objects.make_random_password(length=12)
            calendar.save()
            messages.success(request, '招待URLが変更されました')
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



