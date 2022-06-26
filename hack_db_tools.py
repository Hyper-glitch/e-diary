"""Module helps to interact with e-diary database and change there data"""
import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Lesson, Commendation, Schoolkid, Teacher, Subject

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


def create_commendation(subject: str, year_of_study: int, schoolkid_name: str, teacher: Teacher):
    """Create commendation for given subject and schoolkid.
    Args:
        subject: mathematics, Russian, etc. - tied to the year of study.
        year_of_study: current year of study.
        schoolkid_name: schoolkid's name.
        teacher: obj from database.
    Returns:
        None
    """
    try:
        subject_obj = Subject.objects.get(title=subject, year_of_study=year_of_study)
    except ObjectDoesNotExist:
        print(f'There is no one subject - {subject}! Probably subject title empty or has a mistakes.')
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except MultipleObjectsReturned:
        print(f'There are a lot of  schoolkids with name {schoolkid_name} ! Check full schoolkid name.')
    except ObjectDoesNotExist:
        print(f'There is no one schoolkids with name {schoolkid_name}! Probably full name empty or has a mistakes.')
    else:
        lessons = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject_obj.first().title)
        lesson = random.choice(lessons)
        Commendation.objects.create(
            text=random.choice(COMPLIMENTS), created=lesson.date, schoolkid=schoolkid.first(),
            subject=subject_obj.first(), teacher=teacher.first(),
        )
