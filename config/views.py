from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def SPA(request, *args, **kwargs):
    return render(request, 'SPA.html')
