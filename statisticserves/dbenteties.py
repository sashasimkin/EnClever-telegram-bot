import mongoengine
import datetime


mongoengine.connect("english_bot_db")


class Statistic(mongoengine.EmbeddedDocument):
    visits_in_row = mongoengine.DecimalField()
    first_day_visit = mongoengine.DateTimeField()


class FlashCard(mongoengine.Document):
    pic = mongoengine.StringField()
    topic = mongoengine.StringField()
    complexity_level = mongoengine.DecimalField()


class UserFlashCard(mongoengine.EmbeddedDocument):
    flash_card = mongoengine.ReferenceField(FlashCard)
    state = mongoengine.DecimalField(required=True)
    last_appearance = mongoengine.DateTimeField()


class User(mongoengine.Document):
    chat_id = mongoengine.DecimalField(primary_key=True, required=True)
    first_name = mongoengine.StringField(max_length=50)
    last_name = mongoengine.StringField(max_length=50)
    cards = mongoengine.ListField(mongoengine.EmbeddedDocumentField(UserFlashCard))
    statistic = mongoengine.EmbeddedDocumentField(Statistic)
    last_appearance = mongoengine.DateTimeField()

