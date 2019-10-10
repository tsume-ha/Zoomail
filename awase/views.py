from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

@login_required()
def index(request):
    display_date = (
        datetime.date(2019,10,10),
        datetime.date(2019,10,11),
        datetime.date(2019,10,12),
        datetime.date(2019,10,13),
        datetime.date(2019,10,14),
        datetime.date(2019,10,15),
        datetime.date(2019,10,16),
        )
    params = {
        'timetuple': (n for n in range(9,27)),
        'datetuple': display_date,
    }
    return render(request, 'awase/index.html', params)