# unit tests
import random


def get_sentence():
    f = open('fortests.txt').read()
    sentences = f.split('\n')
    sentence = random.choice(sentences)
    return sentence


def test_get_sentence():  ## корректно ли функция get_sentence берёт предложения
    sentences = ['sentence1', 'sentence2', 'sentence3', 'sentence with spaces', 'sentence with, and.']
    sentence = get_sentence()
    if sentence in sentences:
        return 1
    else:
        return 0


if test_get_sentence() == 1:
    print("OK")
else:
    print("Error")
