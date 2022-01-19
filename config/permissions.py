from members.models import User

# kansou
def KansouPermission(user):
    return user.has_perm("kansou.add_kansouyoushi")


# members
def MemberRegisterPermission(user):
    return user.has_perm("members.change_user")


def AdminEnterPermission(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Administer").exists()
        or user.groups.filter(name="HomepageGroup").exists()
    )


# pictures
def PicturesPermission(user):
    return user.has_perm("pictures.add_album")


# sound
def RecordingPermisson(user):
    return user.has_perm("sound.add_live") or user.has_perm("sound.add_song")


# other documents
def OtherDocsPermission(user):
    return user.has_perm("otherdocs.view_content")


# meeting room
def MeetingroomPermission(user):
    return user.has_perm("meeting_room.add_cashe")
