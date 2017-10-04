from mongoengine import *
import datetime
import settings

connect("enclever_test", host=settings.MONGO_DB_URI)  # тестовая  БД

BOTTOM_GROUP = 1
MIDDLE_GROUP = 2
TOP_GROUP = 3

TOP_GROUP_REPEAT_INTERVAL = 5
MIDDLE_GROUP_REPEAT_INTERVAL = 3
BOTTOM_GROUP_REPEAT_INTERVAL = 1


class FlashCard(Document):
    """
    FlashCard затычка
    """
    term = StringField(required=True)
    term_native = StringField(required=True)  # In russian
    description = StringField(required=True)
    pic = StringField(required=True)  # URL/path to the image


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
        flash_card = FlashCard(term="CardTerm: " + str(i), term_native=str(i), description="Description",
                               pic="picture:")
        flash_card.save()
        dummy_cards.append(flash_card)
    return dummy_cards


def add_single_card_to_box(card):
    """
    Добавляет карточку в коробку для повторений
    :param card: флеш карта для повторения
    """
    if len(RepeatBox.objects(flash_card_id=card.id)) == 0:  # проверка, есть ли карта в коробке
        card_in_box = RepeatBox(flash_card_id=card.id, group=BOTTOM_GROUP, date_to_repeat=datetime.date.today())
        card_in_box.save()
    else:
        print("Card already in BOX")


def delete_card_from_box(card):
    """
    Удаляет карту из коробки
    :param card: карта для удаления
    """
    try:
        card_in_box = RepeatBox.objects.get(flash_card_id=card.id)
        card_in_box.delete()
    except DoesNotExist:
        print("Карты нет в БД для повторения")


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


def check_user_answer(card, answer):
    """
    :param card: карточка заданная пользователю
    :param answer: ответ пользователя
    """
    card_in_box = RepeatBox.objects.get(flash_card_id=card.id)  # Обьект, в коробке для повторения, с id карточки
    interval_to_repeat = BOTTOM_GROUP_REPEAT_INTERVAL  # по умолчания интервал повторения каждый день
    if card.term_native == answer:
        print("Correct")
        if card_in_box.group < TOP_GROUP:  # если карточка ещё не в верхнем(3) уровне, продвигаем её на верх
            card_in_box.group += 1
        if card_in_box.group == MIDDLE_GROUP:  # устанавливает интервал повторения соответсвующий группе 2 (раз в 3 дня)
            interval_to_repeat = MIDDLE_GROUP_REPEAT_INTERVAL
        if card_in_box.group == TOP_GROUP:  # устанавливает интервал повторения соответсвующий группе 2 (раз в 5 дней)
            interval_to_repeat = TOP_GROUP_REPEAT_INTERVAL
    else:  # если ответ не верный, сбрасываем карточку на 1ый уровень, интервал повторений - каждый день
        print("Incorrect")
        card_in_box.group = BOTTOM_GROUP
    card_in_box.date_to_repeat += datetime.timedelta(days=interval_to_repeat)  # дата, когда повторить карточку
    card_in_box.save()


if __name__ == '__main__':
    if len(FlashCard.objects()) == 0:  # если БД пуста, заполняет ему dummy картами
        dummy_card_list = generate_dummy_cards()
        add_cards_to_box(dummy_card_list)
    else:
        dummy_card_list = FlashCard.objects()

    for card_in_box in get_cards_to_repeat():
        card = FlashCard.objects.get(id=card_in_box.flash_card_id)
        print(card.term)
        answer = input("Введите ответ (№)")  # Ответом является номер карточки
        check_user_answer(card, answer)
        print("*" * 20)
