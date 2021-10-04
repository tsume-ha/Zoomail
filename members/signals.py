from django.db.models import Q
from django.contrib.auth.models import Group, Permission

def create_default_group(sender, **kwargs):
    kanbu, kanbu_creted = Group.objects.get_or_create(name='幹部')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        
        Q(codename='add_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='change_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='delete_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='view_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        
        Q(codename='change_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='delete_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='view_user', content_type__app_label='members', content_type__model='user') |
        
        Q(codename='add_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='change_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='delete_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='view_content', content_type__app_label='otherdocs', content_type__model='content')
    )
    kanbu.permissions.set(permission_list)

    HP, HP_created = Group.objects.get_or_create(name='HP')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        
        Q(codename='add_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='change_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='delete_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='view_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        
        Q(codename='change_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='delete_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='view_user', content_type__app_label='members', content_type__model='user') |
        
        Q(codename='add_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='change_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='delete_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='view_content', content_type__app_label='otherdocs', content_type__model='content') |

        Q(codename='add_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='change_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='delete_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='view_album', content_type__app_label='pictures', content_type__model='album') |

        Q(codename='add_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='change_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='delete_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='view_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='add_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='change_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='delete_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='view_song', content_type__app_label='sound', content_type__model='song') |
        
        Q(codename='add_youtubeurl', content_type__app_label='movie', content_type__model='youtubeurl') |
        Q(codename='change_youtubeurl', content_type__app_label='movie', content_type__model='youtubeurl') |
        Q(codename='delete_youtubeurl', content_type__app_label='movie', content_type__model='youtubeurl') |
        Q(codename='view_youtubeurl', content_type__app_label='movie', content_type__model='youtubeurl') |
        
        Q(codename='add_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='change_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='delete_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='view_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |

        Q(codename='add_announcement', content_type__app_label='home', content_type__model='announcement') |
        Q(codename='change_announcement', content_type__app_label='home', content_type__model='announcement') |
        Q(codename='delete_announcement', content_type__app_label='home', content_type__model='announcement') |
        Q(codename='view_announcement', content_type__app_label='home', content_type__model='announcement')
    )
    HP.permissions.set(permission_list)

    meetingroom, meetingroom_creted = Group.objects.get_or_create(name='教室係')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='add_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='change_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='delete_cashe', content_type__app_label='meeting_room', content_type__model='cashe') |
        Q(codename='view_cashe', content_type__app_label='meeting_room', content_type__model='cashe')
    )
    meetingroom.permissions.set(permission_list)

    kansou, kansou_creted = Group.objects.get_or_create(name='感想用紙')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='add_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='change_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='delete_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='view_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi')
    )
    kansou.permissions.set(permission_list)

    PA, PA_creted = Group.objects.get_or_create(name='PA')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='add_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='change_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='delete_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        Q(codename='view_kansouyoushi', content_type__app_label='kansou', content_type__model='kansouyoushi') |
        
        Q(codename='change_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='delete_user', content_type__app_label='members', content_type__model='user') |
        Q(codename='view_user', content_type__app_label='members', content_type__model='user') |
        
        Q(codename='add_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='change_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='delete_content', content_type__app_label='otherdocs', content_type__model='content') |
        Q(codename='view_content', content_type__app_label='otherdocs', content_type__model='content') |

        Q(codename='add_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='change_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='delete_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='view_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='add_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='change_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='delete_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='view_song', content_type__app_label='sound', content_type__model='song')
    )
    PA.permissions.set(permission_list)

    photo, photo_creted = Group.objects.get_or_create(name='写真係')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='add_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='change_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='delete_album', content_type__app_label='pictures', content_type__model='album') |
        Q(codename='view_album', content_type__app_label='pictures', content_type__model='album')
    )
    photo.permissions.set(permission_list)

    recording, recording_creted = Group.objects.get_or_create(name='録音係')
    permission_list = Permission.objects.filter(
        Q(codename='view_logentry', content_type__app_label='admin', content_type__model='logentry') |
        Q(codename='change_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='view_group', content_type__app_label='auth', content_type__model='group') |
        Q(codename='add_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='change_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='delete_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='view_live', content_type__app_label='sound', content_type__model='live') |
        Q(codename='add_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='change_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='delete_song', content_type__app_label='sound', content_type__model='song') |
        Q(codename='view_song', content_type__app_label='sound', content_type__model='song')
    )
    recording.permissions.set(permission_list)

