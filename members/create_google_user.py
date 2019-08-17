from members.models import User
from social_django.models import AbstractUserSocialAuth as SocialModel


def Create_Google_User(email, year=0, first_name=None, last_name=None):
    user = User.objects.create_user(email, year)
    content = SocialModel(
        user = user,
        provider = 'Google OAuth 2',
        uid = email,
        )
    content.save()