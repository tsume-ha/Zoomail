# from members.models import User
from social_django.models import UserSocialAuth

def run():
    for content in UserSocialAuth.objects.all():
        user = content.user
        if content.provider == 'google-oauth2':
            user.google_login = True
            user.save()
        if content.provider == 'auth0':
            user.livelog_login = True
            user.save()
