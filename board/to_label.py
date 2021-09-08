def label(item):
    if item.year == 0:
        return item.label
    if 2000 < item.year < 2100:
        if item.label:
            return item.label
        if item.leader:
            return "{} {}期（会長：{}）".format(item.year, item.year-1994, item.leader.get_full_name())
        if not item.leader:
            return "{} {}期".format(item.year, item.year-1994)