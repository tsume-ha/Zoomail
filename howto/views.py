from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required()
def index(request):
    return render(request, "howto/index.html")


# @login_required()
def user_setting(request):
    return render(request, "howto/user_setting.html")


# @login_required()
def send_message(request):
    return render(request, "howto/send_message.html")


# @login_required()
def introduction(request):
    return render(request, "howto/introduction.html")


# @login_required()
def login(request):
    return render(request, "howto/login.html")


@login_required()
def otherdocs(request):
    return render(request, "howto/otherdocs.html")
