import re, os, csv
from nltk.tokenize import sent_tokenize, word_tokenize


#####################################################################


our_dir = "texts-in-subdirs/"


#####################################################################


def full_paths():
    list_of_full_paths = []
    for path, subdirs, files in os.walk(our_dir):
        for each in files:
            list_of_full_paths.append(os.path.join(path, each))
    return list_of_full_paths

paths = full_paths()


#####################################################################


def words_count(text):
    preout = word_tokenize(text)
    out = []
    for i in preout:
        if i not in ",.–?—.—":
            clear_word = re.sub( "\W", "", i)
            if len(clear_word) > 0:
                out.append(clear_word.lower())
    return len(out)


#####################################################################


# http://stackoverflow.com/a/10840586
try:
    os.remove("sentence-length.csv")
except OSError:
    pass

with open('sentence-length.csv', 'a', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(('country', 'mean.words.in.sentence', 'number.of.tales'))

    for path, subdirs, files in os.walk(our_dir):
        if len(files) != 0:
            lengths = []
            number_of_tales = 0
            for each in files:
                #print(each)
                number_of_tales = len(files)
                with open (os.path.join(path, each), encoding = 'utf8') as file:
                    example_text = file.read()
                    sentences = sent_tokenize(example_text)
                    for i in sentences:
                        needed = words_count(i)
                        lengths.append(needed)
            mean_length = sum(lengths) / len(lengths)
            mean_length_output = float("{0:.1f}".format(mean_length))
            country = path[len(our_dir):]
            #country = path[9:].split("-")[0]
            #country = country.split("_")[0]
            print(country)
            print(mean_length_output)
            print(number_of_tales)
            a.writerow((country, mean_length_output, number_of_tales))
            print("\n")


#####################################################################
