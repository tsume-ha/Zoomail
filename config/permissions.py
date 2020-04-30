from members.models import User

# kansou
def KansouPermission(user):
    return user.has_perm('kansou.add_kansouyoushi')


# members
def MemberRegisterPermission(user):
    return user.has_perm('members.change_user')

def AdminEnterPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists() or\
           user.groups.filter(name='HomepageGroup').exists()


# pictures
def PicturesPermission(user):
    return user.has_perm('pictures.add_album')


# player
def RecordingPermisson(user):
    return user.has_perm('player.add_performance') or\
           user.has_perm('player.add_song')


# other documents
def OtherDocsPermission(user):
    return user.has_perm('otherdocs.add_content') or\
           user.has_perm('otherdocs.change_content')
