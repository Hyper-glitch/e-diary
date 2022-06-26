import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Lesson, Commendation, Schoolkid


def fix_marks(schoolkid):
    """Filter marks, that less than 4 point for current schoolkid and replace value for excellent mark."""
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    """Filter chastisement for current schoolkid and delete all of them."""
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid.first())
    chastisement.delete()


def create_commendation(subject, text, schoolkid_name, teacher):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except MultipleObjectsReturned:
        print(f'There are schoolkids with name {schoolkid_name} more than one!')
    except ObjectDoesNotExist:
        print(f'There is no one schoolkids with name {schoolkid_name}!')
    else:
        lessons = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject.first().title)
        lesson = random.choice(lessons)
        Commendation.objects.create(
            text=text, created=lesson.date, schoolkid=schoolkid.first(),
            subject=subject.first(), teacher=teacher.first(),
        )
