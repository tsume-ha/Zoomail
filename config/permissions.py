# kansou
def KansouPermission(user):
    return user.has_perm("kansou.add_kansouyoushi")


# members
def MemberRegisterPermission(user):
    return user.has_perm("members.change_user")


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
def MeetingRoomRegisterPermission(user):
    return user.has_perm("meeting_room.add_room")
