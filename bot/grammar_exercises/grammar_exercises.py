from random import randint, shuffle, choice
import re
from word_forms.word_forms import get_word_forms

PUNCTUATION = """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
ATTEMPTS = 3
CHOICES = 10
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
    return words


#заглушка на выбор слова по правилу
def wrest_a_word(sentence):
    words = get_words(sentence)
    word_ind = randint(0, len(words) - 1)
    word = words[word_ind]
    words = sentence.split()
    words[word_ind] = "*****"
    sentence = ' '.join(words)
    return word, sentence


def get_random_words(initial_word, random_sentences):
    result = [initial_word]
    initial_word_forms = get_word_forms(initial_word)
    for word in initial_word_forms:
        if word not in result:
            result.append(word)
    result.append(initial_word_forms)
    while len(result) < CHOICES*2:
        for sentence in random_sentences:
            words = get_words(sentence[0])
            for word in words:
                if word not in result:
                    result.append(word)
    result = result[1:]
    shuffle(result)
    result = result[CHOICES-1]
    result.append(initial_word)
    shuffle(result)
    return result


#заглушка для ввода данных
def get_user_input():
    return input()


#заглушка для статистики
def store_result():
    pass


class GExercise:
    def __init__(self, example_list):
        sentences = choice(example_list)
        self.sentence_en = sentences[0]
        self.sentence_ru = sentences[1]

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
        self.words = get_words(self.sentence_en)
        shuffle(self.words)

    def ask_user(self):
        print("Предложение на русском языке:\n"
              "{}".format(self.sentence_ru))
        print("Составь это предложение на английском языке, используя эти слова:\n"
              "{}".format(tuple(self.words)))

    def check_answer(self, answer):
        print('ha')


class InsertWord(GExercise):
    def __init__(self, example_list):
        GExercise.__init__(self, example_list)
        info = wrest_a_word(self.sentence_en)
        self.word_a = info[0]
        self.sentence_en_mod = info[1]
        self.words = get_random_words(self.word_a, example_list)

    def ask_user(self):
        print("Предложение на русском языке:\n"
              "{}".format(self.sentence_ru))
        print("В этом предложении пропущено слово:\n"
              "{}".format(tuple(self.sentence_en_mod)))
        print("Вот доступные слова для подстановки:\n"
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
    words = ['gave', 'went', 'going', 'dating', 'frozen', 'me', 'running', 'kitchen', 'rock']
    for word in words:
        print(get_word_forms(word))
    do_exercise(InsertWord)

