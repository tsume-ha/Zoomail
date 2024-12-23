from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Message


@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(to_groups__year=0)
        | Q(to_groups__year=request.user.year)
        | Q(sender=request.user)
        | Q(writer=request.user)
    ).distinct()

    context = {
        "messages": messages,
    }
    return render(request, "mail/inbox.html", context)
