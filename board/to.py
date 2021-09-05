from .models import To
from .to_label import label

to_groups = [
    (item.year, label(item)) for item in To.objects.all().order_by("year")
]

