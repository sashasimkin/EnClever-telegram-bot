from random import randint, shuffle
import re
from word_forms.word_forms import get_word_forms

PUNCTUATION = """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
ATTEMPTS = 3
#Затычка: набор предложений под какое-то правило
examples = [["What a fantastic view.", "Какой фантастический вид."],
            ["What a beautiful dress!", "Какое красивое платье!"],
            ["Everybody looks so happy.", "Все выглядят такими счастливыми."],
            ["Everything is so beautiful!", "Всё такое красивое!"],
            ["I missed all the signs.", "Я пропустила все знаки."],
            ["I know something.", "Я знаю что-то."],
            ["You need help.", "Вы нуждаетесь в помощи."],
            ["I've been playing it all day.", "Я играю в это весь день."],
            ]


def remove_punctuation(sentence):
    return re.sub('[' + PUNCTUATION + ']', '', sentence)


def get_words(sentence):
    words = remove_punctuation(sentence).split()
    shuffle(words)
    return words


#заглушка для ввода данных
def get_user_input():
    return input()


#заглушка для статистики
def store_result():
    pass


class GExercise:
    def __init__(self, example_list):
        sentences = example_list[randint(0, len(example_list)-1)]
        self.sentence_en = sentences[0]
        self.sentence_ru = sentences[1]
        self.words = get_words(self.sentence_en)

    def check_answer(self, answer):
        answer = answer.lower()
        answer = remove_punctuation(answer)
        initial_sentence = remove_punctuation(self.sentence_en.lower())
        if initial_sentence == answer:
            return True
        else:
            return False


class PhraseConstructor(GExercise):
    def __init__(self, example_list):
        GExercise.__init__(self, example_list)

    def ask_user(self):
        print("Предложение на русском языке:\n"
              "{}".format(self.sentence_ru))
        print("Составь это предложение на английском языке, используя эти слова:\n"
              "{}".format(tuple(self.words)))


def do_exercise(exercise_class):
    exercise = exercise_class(examples)
    exercise.ask_user()
    failed_attempts = 0
    while failed_attempts < ATTEMPTS:
        answer = get_user_input()
        if exercise.check_answer(answer):
            print("Круто. У тебя получилось!")
            store_result()
            break
        else:
            print("Неверно. Попробуй еще раз.")
            failed_attempts += 1
    if failed_attempts == ATTEMPTS:
        print("Не получилось.\n"
              "Правильный ответ: {}".format(exercise.sentence_en))


if __name__ == '__main__':
    do_exercise(PhraseConstructor)
    #test
    print(get_word_forms("run"))
