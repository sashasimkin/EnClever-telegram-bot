import datetime
from enum import Enum


class State(Enum):
    Learned = 1
    Skipped = 2
    Pending = 3

def user_entry(user):
    last_visit = user.statistics.first_day_visit.date()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if last_visit == yesterday:
        user.statistics.first_day_visit = datetime.datetime.now()
        user.statistics.visits_in_row += 1
    elif yesterday > last_visit:
        user.statistics.first_day_visit = datetime.datetime.now()
        user.statistics.visits_in_row = 1
    user.save()

def user_learned(user):
    return user.cards(state=State.Learned).count()

def user_skipped(user):
    return user.cards(state=State.Skipped).count()

def user_progress(user):
    return "{}%".format(user_learned(user) / user.cards().count() * 100)

def visits_in_row(user):
    return user.statistics.visits_in_row
