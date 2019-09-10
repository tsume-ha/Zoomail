from members.models import User
from social_django.models import UserSocialAuth
from django.db.utils import IntegrityError

class DuplicateGmailAccountError(Exception):
    pass
        

def Create_Google_User(email, year=0, first_name='', last_name='', furigana=''):
    try:
        user = User.objects.create_user(email, year)
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if furigana != '':
            user.furigana = furigana
        user.save()

        content_social = UserSocialAuth(
            user = user,
            provider = 'google-oauth2',
            uid = email,
            )
        content_social.save()
    except IntegrityError:
        raise DuplicateGmailAccountError('すでに登録されているGoogleアカウントです')
