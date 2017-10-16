from mongoengine import *


class User(Document):

    chat_id = IntField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    cards = ListField(EmbeddedDocumentField(UserFlashCard))
    statistic = EmbeddedDocumentField(Statistic)
    last_appearance = DateTimeField()
    target_complexity = IntField()

class UserFlashCard(EmbeddedDocument):

    flash_card = ReferenceField(FlashCard, required=True)
    learn_state = IntField()
    box = ReferenceField(RepeatBox)
    
class FlashCard(EmbeddedDocument):

    term = StringField(required=True)
    term_native = StringField(required=True)
    transcription = StringField()
    description = StringField()
    pic = StringField()
    example = StringField()
    topic = StringField()
    complexity = IntField()
    
class RepeatBox(Document):
    
    level = IntField()
    interval = IntField()
    
class Statistic(EmbeddedDocument):

    visits_in_row = IntField()
    first_in_row = DateTimeField()
