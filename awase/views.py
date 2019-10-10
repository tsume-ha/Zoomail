from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
    params = {
        'display_time': (n for n in range(9,27)),
    }
    return render(request, 'awase/index.html', params)