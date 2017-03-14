import re, nltk, random, os
from nltk import ngrams
from pymystem3 import Mystem
from easygui import *
from random import randint, shuffle


####################################################################
#                                                                  #
# Создадим список стран (поддиректорий) с числом сказок (файлов)   #
#                                                                  #
####################################################################

our_dir = "texts-in-subdirs/"

subdirs = os.listdir(our_dir) # list of subdirectories
talesList = []
for directory in subdirs:
    talesList.append(str(directory) + " сказки (" + str(len(os.listdir(our_dir + directory))) + " шт.)")


################################
#                              #
# Игрок выбирает две страны    #
#                              #
################################

msg = "Выберите первую страну:"
title = "Игра"
choices = talesList
first_choice = choicebox(msg, title, choices)
first_choice_index = talesList.index(first_choice)
talesList.remove(first_choice)

print(first_choice)

country_first_choice = first_choice[:first_choice.find(' ')].lower() # Название первой страны без штук.
shtuk_first_choice = first_choice[first_choice.find('('):] # Количество сказок в штуках в скобках без названия страны.

msg = "Первая страна: " + country_first_choice + " " + shtuk_first_choice + "\nВыберите вторую страну:"
title = "Игра"
choices = talesList
second_choice = choicebox(msg, title, choices)
second_choice_index = talesList.index(second_choice)
if second_choice_index >= first_choice_index:
    second_choice_index = second_choice_index + 1

print(second_choice)

#print("первая выбранная страна:", our_dir + subdirs[first_choice_index])
#print("вторая выбранная страна:", our_dir + subdirs[second_choice_index])



################################
#                              #
# Все тексты сказок в 1 строку #
#                              #
################################

def subdir_to_text(choice):
    texts = []
    for filename in os.listdir(our_dir + subdirs[choice]):
            with open(our_dir + subdirs[choice] + "/" + filename, encoding = "utf-8") as infile:
                texts.append(infile.read())

    first_tales = '\n\n'.join(texts)
    return first_tales


#print(subdir_to_text(first_choice_index))
#print("\n\n\n\n\n\n")
#print(subdir_to_text(second_choice_index))


################################
#                              #
#  Очистим текст от лишнего    #
#                              #
################################


def clean_string(group):
    # http://stackoverflow.com/a/35614234 Removing punctuation except intra-word dashes Python
    p = re.compile(r'(\b[-]\b)|[\W_]')  # уберём всю пунктуацию, но оставим внутрисловные дефисы, часть 1
    clean = p.sub(lambda m: (m.group(1) if m.group(1) else ' '), group)  # уберём всю пунктуацию, но оставим внутрисловные дефисы, часть 2
    clean = re.sub(r'\d+', '', clean) # удалим цифры (в сказках их нет, но в общем случае могут быть)
    clean = re.sub(r'[ ]+', ' ', clean)  # заменим много пробелов подряд одним пробелом
    clean = clean.lower()  # заменим большие буквы на маленькие
    return clean



initialTextFIR = clean_string(subdir_to_text(first_choice_index))
initialTextSEC = clean_string(subdir_to_text(second_choice_index))

#print(initialTextFIR)
#print(initialTextSEC)



################################
#                              #
# Игрок вводит N для N-грамм   #
#                              #
################################



N = integerbox(msg = "Из скольки слов показывать фразы?",
               title = "Игра",
               default = 3,
               lowerbound = 1)

print("N =", N)

numberOfPhrasesInGame = 7

print("Количество ходов в игре:", numberOfPhrasesInGame)



##################################################
#                                                #
# Надписи кнопок куда игрок будет относить фразы #
#                                                #
##################################################


m = Mystem()

firstLang = str(first_choice.split(" ")[0] )[:-2] + "ая" + " сказка"

secondLang = str(second_choice.split(" ")[0] )[:-2] + "ая" + " сказка"



#####################################################################
#                                                                   #
# Первая страна: лемматизируем, строим N-грамы и записываем частоты #
#                                                                   #
#####################################################################


lemmatizedTextFIR = m.lemmatize(initialTextFIR)
afterLemmatizationFIR = ''.join(lemmatizedTextFIR)
#print(afterLemmatizationFIR)

myNgramFIR = ngrams(afterLemmatizationFIR.split(), N)
listOfNgrammsFIR=[]
for gram in myNgramFIR:
    listOfNgrammsFIR.append(gram)

fdistFIR = nltk.FreqDist(listOfNgrammsFIR)

ngramsForGameFIR = []
statsFIR = []
for word, frequency in fdistFIR.most_common(numberOfPhrasesInGame):
    ngramsForGameFIR.append("{} {}".format(word, frequency))
    statsFIR.append("{} {}".format(word, frequency)) # чтобы показать в конце игры статистику



#####################################################################
#                                                                   #
# Вторая страна: лемматизируем, строим N-грамы и записываем частоты #
#                                                                   #
#####################################################################


lemmatizedTextSEC = m.lemmatize(initialTextSEC)
afterLemmatizationSEC = ''.join(lemmatizedTextSEC)
#print(afterLemmatizationSEC)


myNgramSEC = ngrams(afterLemmatizationSEC.split(), N)
listOfNgrammsSEC=[]
for gram in myNgramSEC:
    listOfNgrammsSEC.append(gram)

fdistSEC = nltk.FreqDist(listOfNgrammsSEC)

ngramsForGameSEC = []
statsSEC = []
for word, frequency in fdistSEC.most_common(numberOfPhrasesInGame):
    ngramsForGameSEC.append("{} {}".format(word, frequency))
    statsSEC.append("{} {}".format(word, frequency)) # чтобы показать в конце игры статистику



######################################################
#                                                    #
# Удалим пунктуацию и числа из списков фраз для игры #
#                                                    #
######################################################

# http://stackoverflow.com/a/6130251
for index, item in enumerate(ngramsForGameFIR):
    item = re.sub(r"[,)('\d]+", "", item)[:-1]
    ngramsForGameFIR[index] = item
for index, item in enumerate(ngramsForGameSEC):
    item = re.sub(r"[,)('\d]+", "", item)[:-1]
    ngramsForGameSEC[index] = item



###########################################################
#                                                         #
# Перйдём от лемматизированных фраз к нелемматизированным #
#                                                         #
###########################################################

def backToOriginalPhrases(initialText, afterLemmatization, ngramsForGame):

    # Step 1
    # разбиваем лемматизированный текст на N-граммы
    ngrams_lemmatizedFIR = []
    generator = ngrams(afterLemmatization.split(), N) # class generator
    for i in generator:
        ngrams_lemmatizedFIR.append(i)

    ngrams_lemmatized_str = []
    for each in ngrams_lemmatizedFIR:
        clean = re.sub(r"[(',)]", "", str(each))
        ngrams_lemmatized_str.append(clean)


    # Step 3
    # найдём номера нужной N-граммы среди всех лемматизированных

    print(ngramsForGame)
    ngrams_to_show = []
    for key in ngramsForGame:
        searched_ngram = []
        for (i, subw) in enumerate(ngrams_lemmatized_str):
            if (subw == key):
                searched_ngram.append(i + 1)

        # Step 4
        # случайно выберем один из вариантов встречания искомой N-граммы
        choosen_init_variant = random.choice(searched_ngram)

        # Step 5
        # нелемматизированный текст разбиваем на N-граммы
        ngrams_initial = []
        generat = ngrams(initialText.split(), N)
        for i in generat:
            ngrams_initial.append(i)

        # Step 6
        # берём ту нелемматизированную N-грамму по номеру из шага 4
        text_to_show = ' '.join(ngrams_initial[choosen_init_variant - 1])

        # Step 7
        # создаем
        ngrams_to_show.append(text_to_show)

    return(ngrams_to_show)



ngrams_to_show_FIR = backToOriginalPhrases(initialTextFIR, afterLemmatizationFIR, ngramsForGameFIR)
print(ngrams_to_show_FIR)


ngrams_to_show_SEC = backToOriginalPhrases(initialTextSEC, afterLemmatizationSEC, ngramsForGameSEC)
print(ngrams_to_show_SEC)



##################################
#                                #
# Удаляем общие элемениы списков #
#                                #
##################################

ngrams_to_show_FIR = set(ngrams_to_show_FIR) - set(ngrams_to_show_SEC)

ngrams_to_show_SEC = set(ngrams_to_show_SEC) - set(ngrams_to_show_FIR)



##############################################################
#                                                            #
# Помечаем и перемешиваем нелемматизированные фразы для игры #
#                                                            #
##############################################################

markedngramForGameFIR = ["FIR" + i for i in ngrams_to_show_FIR]

markedNgramForGameSEC = ["SEC" + i for i in ngrams_to_show_SEC]

BothNgrams = markedngramForGameFIR + markedNgramForGameSEC

shuffle(BothNgrams)

print("\n" + str(BothNgrams))



##############################################
#                                            #
#   Игрок отвечает на фразы и ведётся счёт   #
#                                            #
##############################################

count = 0
winstat = 0

while count < len(ngramsForGameFIR):

    k = randint(1, numberOfPhrasesInGame)

    msg = BothNgrams[ k ] #элемент из перемешанного списка без первых трех букв

    choices = [firstLang, secondLang]

    reply = buttonbox(msg[3:],
                      title = "Игра",
                      choices = choices)

    if (reply == firstLang and str(BothNgrams[ k ])[:3] == "FIR"):

        BothNgrams.remove(msg)  # чтобы не выводить дважды одну и ту же фразу

        winstat += 1

        msgbox(msg = "Вы молодец!", title = "Игра")

    elif (reply == secondLang and str(BothNgrams[k])[:3] == "SEC"):

        BothNgrams.remove(msg)  # чтобы не выводить дважды одну и ту же фразу

        winstat = winstat + 1

        msgbox(msg = "Вы молодец!", title = "Игра")

    else:

        BothNgrams.remove(msg)  # чтобы не выводить дважды одну и ту же фразу

        msgbox(msg = "А вот и нет.", title = "Игра")

    count += 1



#########################################
#                                       #
# Последнее окошко игры, со статистикой #
#                                       #
#########################################

statsFIR = "\n".join(statsFIR) # сделаем из листа в строку
statsSEC = "\n".join(statsSEC) # сделаем из листа в строку

msgbox(msg =   "                    " + "Вы угадали " + str(winstat) + " из " + str(numberOfPhrasesInGame) + "\n"
             + "\n"
             + "Топ-" + str(numberOfPhrasesInGame) + " лемматизированных " + str(N) + "-грамм по странам:" + "\n"
             + "\n"
             + "                    " + first_choice + "\n"
             + statsFIR + "\n"
             + "\n"
             + "                    " + second_choice + "\n"
             + statsSEC + "\n"
             + "\n"
             + "            " + "http://www.fairy-tales.su/narodnye/",
       title = "Статистика",
       image = "mickey.gif",
       ok_button = "Выход")

