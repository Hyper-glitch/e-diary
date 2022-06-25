from datacenter.models import Mark, Chastisement


def fix_marks(schoolkid):
    """Filter marks, that less than 4 point for current schoolkid and replace value for excellent mark."""
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    """Filter chastisement for current schoolkid and delete all of them."""
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid[0])
    chastisement.delete()
