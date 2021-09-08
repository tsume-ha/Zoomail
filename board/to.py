from .models import To
from .to_label import label

to_groups = [
    (item.year, label(item)) for item in To.objects.filter(year=0)
] + [
    (item.year, label(item)) for item in To.objects.filter(year__gt=0).order_by("year").reverse()
]

