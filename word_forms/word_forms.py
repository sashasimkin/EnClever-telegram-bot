try:
    from nltk.corpus import wordnet as wn
    raise_lookuperror_if_wordnet_data_absent = wn.synsets("python")
except LookupError:
    import nltk
    nltk.download("wordnet")
from inflect import engine
from nltk.stem.wordnet import WordNetLemmatizer

from .constants import (ALL_WORDNET_WORDS, CONJUGATED_VERB_LIST,
                        ADJECTIVE_TO_ADVERB)


def belongs(lemma, lemma_list):
    for element in lemma_list:
        if (element.name() == lemma.name() and
                    element.synset() == lemma.synset()):
            return True
    return False


def get_related_lemmas(word):
    all_lemmas_for_this_word = [lemma for ss in wn.synsets(word)
                                for lemma in ss.lemmas()
                                if lemma.name() == word]
    all_related_lemmas = [lemma for lemma in all_lemmas_for_this_word]
    new_lemmas = []
    for lemma in all_lemmas_for_this_word:
        for new_lemma in (lemma.derivationally_related_forms() +
                          lemma.pertainyms()):
            if (not belongs(new_lemma, all_related_lemmas) and
            not belongs(new_lemma, new_lemmas)):
                new_lemmas.append(new_lemma)
    while len(new_lemmas) > 0:
        all_lemmas_for_new_words = []
        for new_lemma in new_lemmas:
            word = new_lemma.name()
            all_lemmas_for_this_word = [lemma for ss in wn.synsets(word)
                                        for lemma in ss.lemmas()
                                        if lemma.name() == word]
            for lemma in all_lemmas_for_this_word:
                if not belongs(lemma, all_lemmas_for_new_words):
                    all_lemmas_for_new_words.append(lemma)
        all_related_lemmas += all_lemmas_for_new_words
        new_lemmas = []
        for lemma in all_lemmas_for_new_words:
            for new_lemma in (lemma.derivationally_related_forms() +
                              lemma.pertainyms()):
                if (not belongs(new_lemma, all_related_lemmas) and
                not belongs(new_lemma, new_lemmas)):
                    new_lemmas.append(new_lemma)
    return all_related_lemmas


def singularize(noun):
    singular = engine().singular_noun(noun)
    if singular in ALL_WORDNET_WORDS:
        return singular
    return noun


def get_word_forms(word):
    word_initial = word
    word = singularize(word)
    word = WordNetLemmatizer().lemmatize(word, 'v')
    related_lemmas = get_related_lemmas(word)
    related_words_dict = {"n" : set(), "a" : set(), "v" : set(), "r" : set()}
    for lemma in related_lemmas:
        pos = lemma.synset().pos()
        if pos == "s":
            pos = "a"
        related_words_dict[pos].add(lemma.name())
    noun_set = [noun for noun in related_words_dict["n"]]
    for noun in noun_set:
        related_words_dict["n"].add(engine().plural_noun(noun))
    verb_set = [verb for verb in related_words_dict["v"]]
    for verb in verb_set:
        for conjugated_verbs in CONJUGATED_VERB_LIST:
            if verb in conjugated_verbs:
                for conjugated_verb in conjugated_verbs:
                    related_words_dict["v"].add(conjugated_verb)
    adjective_set = [adjective for adjective in related_words_dict["a"]]
    for adjective in adjective_set:
        try:
            related_words_dict["r"].add(ADJECTIVE_TO_ADVERB[adjective])
        except KeyError:
            pass
    result = []
    for key in related_words_dict.keys():
        for word in related_words_dict[key]:
            result.append(word)
    return result
