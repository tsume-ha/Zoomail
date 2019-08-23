from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Kansouyoushi
from django.db.models import Max, Min

def KansouPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists() or\
           True


@login_required()
def index(request):
    records = Kansouyoushi.objects.all()
    year_min = records.aggregate(Min('performed_at'))
    year_max = records.aggregate(Max('performed_at'))
    params = {
        'edit_allowed': KansouPermission(user=request.user)
    }
    return render(request, 'kansou/index.html', params)
