from members.models import User

# kansou
def KansouPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists() or\
           user.groups.filter(name='HomepageGroup').exists()

# members
def MemberRegisterPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists() or\
           user.groups.filter(name='HomepageGroup').exists()

def AdminEnterPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists() or\
           user.groups.filter(name='HomepageGroup').exists()


# pictures
def PicturesPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='PhotographersGroup').exists() or\
           user.groups.filter(name='HomepageGroup').exists()


# player
def RecordingPermisson(user):
    return user.is_superuser or \
           user.groups.filter(name='RecordingGroup').exists() or\
           user.groups.filter(name='HomepageGroup').exists()


