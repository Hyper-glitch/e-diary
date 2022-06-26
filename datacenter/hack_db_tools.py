"""Module helps to interact with e-diary database and change there data"""
import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Lesson, Commendation, Schoolkid, Teacher

COMPLIMENTS = [
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
    'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
    'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
    'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
    'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def fix_marks(schoolkid: Schoolkid):
    """Filter marks, that less than 4 point for current schoolkid and replace value for excellent mark.
    Args:
        schoolkid: obj from database
    Returns:
        None
    """
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid: Schoolkid):
    """Filter chastisement for current schoolkid and delete all.
    Args:
        schoolkid: obj from database
    Returns:
        None
    """
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid.first())
    chastisement.delete()


def create_commendation(subject: str, schoolkid_name: str, teacher: Teacher):
    """Create commendation for given subject and schoolkid.
    Args:
        subject: mathematics, Russian, etc. - tied to the year of study.
        schoolkid_name: schoolkid's name.
        teacher: obj from database.
    Returns:
        None
    """
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
            text=random.choice(COMPLIMENTS), created=lesson.date, schoolkid=schoolkid.first(),
            subject=subject.first(), teacher=teacher.first(),
        )
