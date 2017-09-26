from mongoengine import *
import datetime

connect("test")  # тестовая локальная БД


class FlashCard(Document):
    """
    FlashCard затычка
    """
    name = StringField(required=True)
    answer = StringField(max_length=50)


class RepeatBox(Document):
    """
    'Коробка для повторений', содержащая в себе id карточки,
    группу в которой она находится и дату, когда карточку нужно повторить.
    """
    flash_card_id = ObjectIdField(required=True)
    group = DecimalField(required=True)  # группа указывающая, как часто необходимо повторять карточку
    date_to_repeat = DateTimeField(required=True)


def generate_dummy_cards():
    """
    Генерирует объекты затычки типа FlashCard. Сохраняет их в коллекцию
    :return: лист объектов затычек FlashCard
    """
    dummy_cards = []
    dummy_list_size = 5
    for i in range(0, dummy_list_size):
        flash_card = FlashCard(name="CardName:" + str(i),
                               answer="CardAnswer:" + str(100 + i))
        flash_card.save()
        dummy_cards.append(flash_card)
    return dummy_cards


def add_single_card_to_box(card):
    """
    Добавляет карточку в коробку для повторений
    :param card: флеш карта для повторения
    """
    if len(RepeatBox.objects(flash_card_id=card.id)) == 0:  # проверка, есть ли карта в коробке
        card_in_box = RepeatBox(flash_card_id=card.id, group=1, date_to_repeat=datetime.date.today())
        card_in_box.save()
    else:
        print("Card already in BOX")


def add_cards_to_box(card_list):
    """
    Добавляет список карточек в коробку для повторений
    :param card_list:
    """
    for card in card_list:
        add_single_card_to_box(card)


def get_cards_to_repeat():
    """
    :return:  Список карт, дата повторения которых меньше либо равна сегодняшней
    """
    return RepeatBox.objects(date_to_repeat__lte=(datetime.date.today()))


if __name__ == '__main__':
    dummy_card_list = generate_dummy_cards()
    add_cards_to_box(dummy_card_list)

    for card_in_box in get_cards_to_repeat():
        card = FlashCard.objects.get(id=card_in_box.flash_card_id)
        print(card.name)
