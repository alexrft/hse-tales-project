
from pymystem3 import Mystem
import re, csv, os, json

our_dir = "texts-in-subdirs/"

m = Mystem()

# http://stackoverflow.com/a/10840586
try:
    os.remove("part-of-speech.csv")
except OSError:
    pass

with open('part-of-speech.csv', 'a', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(('country',
                'A',
                'ADV',
                'ADVPRO',
                'ANUM',
                'APRO',
                'COM',
                'CONJ',
                'INTJ',
                'NUM',
                'PART',
                'PR',
                'S',
                'SPRO',
                'V',
                'number.of.tales'))

    for path, subdirs, files in os.walk(our_dir):
        if len(files) != 0:
            number_of_tales = 0
            list_of_A = []
            list_of_ADV = []
            list_of_ADVPRO = []
            list_of_ANUM = []
            list_of_APRO = []
            list_of_COM = []
            list_of_CONJ = []
            list_of_INTJ = []
            list_of_NUM = []
            list_of_PART = []
            list_of_PR = []
            list_of_S = []
            list_of_SPRO = []
            list_of_V = []

            for each in files:
                number_of_tales = len(files)
                with open(os.path.join(path, each), encoding='utf8') as file:
                    my_text = file.read()
                    analyzed_text = json.dumps(m.analyze(my_text), ensure_ascii=False)
                    count_A = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("A"), analyzed_text))
                    count_ADV = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("ADV"), analyzed_text))
                    count_ADVPRO = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("ADVPRO"), analyzed_text))
                    count_ANUM = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("ANUM"), analyzed_text))
                    count_APRO = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("APRO"), analyzed_text))
                    count_COM = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("COM"), analyzed_text))
                    count_CONJ = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("CONJ"), analyzed_text))
                    count_INTJ = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("INTJ"), analyzed_text))
                    count_NUM = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("NUM"), analyzed_text))
                    count_PART = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("PART"), analyzed_text))
                    count_PR = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("PR"), analyzed_text))
                    count_S = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("S"), analyzed_text))
                    count_SPRO = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("SPRO"), analyzed_text))
                    count_V = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("V"), analyzed_text))

                    list_of_A.append(count_A)
                    list_of_ADV.append(count_ADV)
                    list_of_ADVPRO.append(count_ADVPRO)
                    list_of_ANUM.append(count_ANUM)
                    list_of_APRO.append(count_APRO)
                    list_of_COM.append(count_COM)
                    list_of_CONJ.append(count_CONJ)
                    list_of_INTJ.append(count_INTJ)
                    list_of_NUM.append(count_NUM)
                    list_of_PART.append(count_PART)
                    list_of_PR.append(count_PR)
                    list_of_S.append(count_S)
                    list_of_SPRO.append(count_SPRO)
                    list_of_V.append(count_V)

            sum_of_A = sum(list_of_A)
            sum_of_ADV = sum(list_of_ADV)
            sum_of_ADVPRO = sum(list_of_ADVPRO)
            sum_of_ANUM = sum(list_of_ANUM)
            sum_of_APRO = sum(list_of_APRO)
            sum_of_COM = sum(list_of_COM)
            sum_of_CONJ = sum(list_of_CONJ)
            sum_of_INTJ = sum(list_of_INTJ)
            sum_of_NUM = sum(list_of_NUM)
            sum_of_PART = sum(list_of_PART)
            sum_of_PR = sum(list_of_PR)
            sum_of_S = sum(list_of_S)
            sum_of_SPRO = sum(list_of_SPRO)
            sum_of_V = sum(list_of_V)

            country = path[len(our_dir):]
            print(country)

            print("A", sum_of_A, ",",
                  "ADV", sum_of_ADV, ",",
                  "ADVPRO", sum_of_ADVPRO, ",",
                  "ANUM", sum_of_ANUM, ",",
                  "APRO", sum_of_APRO, ",",
                  "COM", sum_of_COM, ",",
                  "CONJ", sum_of_CONJ, ",",
                  "INTJ", sum_of_INTJ, ",",
                  "NUM", sum_of_NUM, ",",
                  "PART", sum_of_PART, ",",
                  "PR", sum_of_PR, ",",
                  "S", sum_of_S, ",",
                  "SPRO", sum_of_SPRO, ",",
                  "V", sum_of_V, ",",
                  "number_of_tales", number_of_tales)
            print("\n")

            a.writerow((country,
                        sum_of_A,
                        sum_of_ADV,
                        sum_of_ADVPRO,
                        sum_of_ANUM,
                        sum_of_APRO,
                        sum_of_COM,
                        sum_of_CONJ,
                        sum_of_INTJ,
                        sum_of_NUM,
                        sum_of_PART,
                        sum_of_PR,
                        sum_of_S,
                        sum_of_SPRO,
                        sum_of_V,
                        number_of_tales))

#####################################################################