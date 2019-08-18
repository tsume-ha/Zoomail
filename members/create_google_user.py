from members.models import User
from social_django.models import UserSocialAuth
from django.db.utils import IntegrityError

def Create_Google_User(email, year=0, first_name=None, last_name=None):
    try:
        user = User.objects.create_user(email, year)
        if first_name != None or last_name != None:
            pass # 氏名を登録します。
        content_social = UserSocialAuth(
            user = user,
            provider = 'google-oauth2',
            uid = email,
            )
        content_social.save()
    except IntegrityError:
        print('Regst. Fail : ' + email)
