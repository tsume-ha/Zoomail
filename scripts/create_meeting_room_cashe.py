import datetime
from meeting_room.models import Cashe

def run():
    cashes = []
    start = datetime.date(2021, 1, 1)
    for date in [start + datetime.timedelta(days=i) for i in range(1000)]:
        tmp = Cashe(
            date=date,
            room=None
        )
        cashes.append(tmp)

    Cashe.objects.bulk_create(cashes)
