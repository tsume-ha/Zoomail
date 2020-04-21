from django.contrib import messages

USER_FIELDS = ['username', 'email', 'year']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    if backend.name != 'auth0':
        messages.error(backend.strategy.request, 'あなたのGoogleアカウントは登録されていないため、ログインできませんでいた。')
        return

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return
    
    #nextリンクはsessionに保存されている、これを書き換える
    strategy.session_set('next', '/members/first_register/')
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
