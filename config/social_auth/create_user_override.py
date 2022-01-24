from django.contrib import messages
from django.urls import reverse

USER_FIELDS = ['username', 'email', 'year']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        messages.success(backend.strategy.request, "ログインに成功しました")
        if backend.name == 'auth0':
            user.livelog_login = True
            user.save()
        if backend.name == 'google-oauth2':
            user.google_login = True
            user.save()
        return {'is_new': False}
    if backend.name != 'auth0':
        messages.error(backend.strategy.request, 'あなたのGoogleアカウントは登録されていないため、ログインできませんでいた。')
        return

    # #新入生が入ってくるまでは以下の文でLivrLogアカウントによるユーザー作成を認めない
    # messages.warning(backend.strategy.request,
    #                  '上回生はまず、Googleアカウントでログインしてから紐付け作業を行ってください。くわしくはメーリスをご確認ください。')
    # return
    # #ここまで、新入生が入ってきたら消す

    # 2019よりも上回はLiveLogでの新規登録はさせないように
    if details.get('year') <= 2019:
        messages.warning(
            backend.strategy.request,
            "2019年度入会以上の上回生は、先にGoogleアカウントでログインしてからLiveLogアカウントへの紐付けを行ってください。"
            )
        return

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return
    
    #nextリンクはsessionに保存されている、これを書き換える
    strategy.session_set('next', reverse('first-register'))
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
