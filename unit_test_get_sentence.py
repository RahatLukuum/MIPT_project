# unit tests
import random


def get_sentence():
    f = open('fortests.txt').read()
    sentences = f.split('\n')
    sentence = random.choice(sentences)
    return sentence


def test_get_sentence(personal_test):  ## корректно ли функция get_sentence берёт предложения
    sentences = []
    if personal_test != 0:
        sentences = ['sentence1', 'sentence2', 'sentence3', 'sentence with spaces', 'sentence with, and.']
    else:
        n = int(input("Введите количество предложений, а затем напишите их по одному в строчке: "))
        for i in range(n):
            one_sent = input()
            sentences.append(one_sent)
    sentence = get_sentence()
    if sentence in sentences:
        return 1
    else:
        return 0

personal_test = int(input("Если вы тестируете функцию, выбрав предложения самостоятельно напишите 0, иначе отличное от 0 число: "))
if test_get_sentence(personal_test) == 1:
    print("OK")
else:
    print("Error")
