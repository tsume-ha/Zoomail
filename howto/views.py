from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required()
def index(request):
    return render(request, 'howto/index.html')
   
# @login_required()
def user_setting(request):
    return render(request, 'howto/user_setting.html')