from random import shuffle, choice
import re
from word_forms.word_forms import get_word_forms
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

PUNCTUATION = """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""
ATTEMPTS = 3
CHOICES = 5
GRAMMAR_ADJECTIVES_RULES = ('-est', 'most',)
GRAMMAR_ARTICLES_RULES = ('a', 'an', 'the',)
GRAMMAR_PRONOUNS_RULES = ('indefinite', 'personal', 'possessive',)
GRAMMAR_NUMERALS_RULES = ('numeral',)
GRAMMAR_PREPOSITIONS_RULES = ('preposition',)

#  Затычка под правила
exercises = [
    {
        'rule': "Артикли A, An",
        'theory': "bla-bla-bla",
        'exercises': [["What a fantastic view.", "Какой фантастический вид."],
                      ["What a beautiful dress!", "Какое красивое платье!"],
                      ["It was a brilliant plan.", "Это был великолепный план."],
                      ],
    },
    {
        'rule': "Present Simple +",
        'theory': "bla-bla-bla",
        'exercises': [["I know something.", "Я знаю что-то."],
                      ["You need help.", "Вы нуждаетесь в помощи."],
                      ],
    },
    {
        'rule': "Present Continuous +",
        'theory': "bla-bla-bla",
        'exercises': [["I'm leaving this morning.", "Я уезжаю сегодня утром."],
                      ["You are empowering the child.", "Вы оказываете поддержку ребёнку."],
                      ["I'm heading that way.", "Я направляюсь в ту сторону."],
                      ],
    },
    {
        'rule': "Present Perfect Continuous -",
        'theory': "bla-bla-bla",
        'exercises': [["You haven't been practicing", "Вы не практикуетесь."],
                      ["I haven't been spying.", "Я не шпионю."],
                      ["She hasn't been feeling very well.", "Она чувствует себя не очень хорошо."],
                      ],
    },
    {
        'rule': "Verbs with prepositions",
        'theory': "bla-bla-bla",
        'exercises': [["You look at me.", "Вы смотрите на меня."],
                      ["I worry about you.", "Я беспокоюсь о вас."],
                      ["You count on me.", "Вы рассчитываете на меня."],
                      ],
    },
]


def remove_punctuation(sentence):
    """
    Remove all punctuation marks from a sentence
    """
    return re.sub('[' + PUNCTUATION + ']', '', sentence)


def get_words(sentence):
    """
    Split sentence into words
    """
    words = remove_punctuation(sentence).split()
    return words


def get_rule_class(rule):
    """
    For "Insert word" exercise:
    We need to know which word to wrest from a sentence so it would make sense
    """
    rule = get_words(rule.lower())
    for word in rule:
        if word in GRAMMAR_ADJECTIVES_RULES:
            return "JJ"
        elif word in GRAMMAR_ARTICLES_RULES:
            return "DT"
        elif word in GRAMMAR_PRONOUNS_RULES:
            return "PR"
        elif word in GRAMMAR_NUMERALS_RULES:
            return "CD"
        elif word in GRAMMAR_PREPOSITIONS_RULES:
            return "IN"
    return "VB"


def get_rule_word(sentence, rule):
    """
    Get a word from the sentence depending on the rule
    """
    rule_class = get_rule_class(rule)
    tokenized_words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(tokenized_words)
    for tagged_word in reversed(tagged_words):
        if rule_class in tagged_word[1]:
            return tagged_word[0]
    for tagged_word in reversed(tagged_words):
        if 'N' in tagged_word[1]:
            return tagged_word[0]


def wrest_a_word(sentence, word):
    """
    Get a word from the sentence
    """
    words = sentence.split()
    word_ind = words.index(word)
    words[word_ind] = "*****"
    return ' '.join(words)


def get_random_words(initial_word, random_sentences):
    """
    For "Insert word" exercise:
    Generate a list of words available for insertion
    """
    result = [initial_word]
    initial_word_forms = get_word_forms(initial_word)
    for word in initial_word_forms:
        if word not in result:
            result.append(word)
    while len(result) < CHOICES*2:
        for sentence in random_sentences:
            words = get_words(sentence[0])
            for word in words:
                if word not in result:
                    result.append(word)
    result = result[1:]
    shuffle(result)
    result = result[:CHOICES - 1]
    result.append(initial_word)
    shuffle(result)
    return result


# заглушка для ввода данных
def get_user_input():
    return input()


# заглушка для статистики
def store_result():
    pass


class GExercise:
    def __init__(self, rule, theory, exercises):
        sentences = choice(exercises)
        self.rule = rule
        self.theory = theory
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
    def __init__(self, rule, theory, exercises):
        GExercise.__init__(self, rule, theory, exercises)
        self.words = get_words(self.sentence_en)
        shuffle(self.words)

    # Затычка для общения с юзером
    # ???
    def ask_user(self):
        print("Предложение на русском языке:\n"
              "{}".format(self.sentence_ru))
        print("Составь это предложение на английском языке, используя эти слова:\n"
              "{}".format(tuple(self.words)))


class InsertWord(GExercise):
    def __init__(self, rule, theory, exercises):
        GExercise.__init__(self, rule, theory, exercises)
        self.word_a = get_rule_word(self.sentence_en, self.rule)
        self.sentence_en_mod = wrest_a_word(self.sentence_en, self.word_a)
        self.words = get_random_words(self.word_a, exercises)

    # Затычка для общения с юзером
    # ???
    # Выводить теорию и название правила?
    def ask_user(self):
        print("Предложение на русском языке:\n"
              "{}".format(self.sentence_ru))
        print("В этом предложении пропущено слово:\n"
              "{}".format(self.sentence_en_mod))
        print("Вот доступные слова для подстановки:\n"
              "{}".format(tuple(self.words)))

    def check_answer(self, answer):
        answer = self.sentence_en_mod.replace("*****", answer)
        if answer == self.sentence_en:
            return True
        else:
            return False


def do_exercise(exercise_class):
    task = choice(exercises)
    exercise = exercise_class(task['rule'], task['theory'], task['exercises'])
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
    # Тестирую nltk
    # words = ['gave', 'went', 'going', 'dating', 'frozen', 'me', 'running', 'kitchen', 'rock']
    # for word in words:
    #    print(get_word_forms(word))
    while True:
        do_exercise(InsertWord)
