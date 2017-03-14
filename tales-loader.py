import re, requests, os
from bs4 import BeautifulSoup

our_dir = "texts-in-subdirs/" # В эту директорию будут скачиваться сказки.
ourURL = "http://www.fairy-tales.su/narodnye/" # Страновые сказки будут браться из этого раздела сайта.

def talesLoader():
    landingSoup = BeautifulSoup(requests.get(ourURL).text, "lxml")

    for country in landingSoup.findAll('a', attrs={'href': re.compile("^" + ourURL[len("http://www.fairy-tales.su"): ] + ".+")}):

        countryInRussian = str(country).split('>', 1)[1][:-11] # название страновых сказок на русском языке
        countryInRussian = countryInRussian.split(' ')[0] # потому что иногда там остается пробел
        countryUrl = "http://www.fairy-tales.su" + country.get('href')

        print("\n\n\n-=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- -=- ")
        print("Сейчас начнут скачиваться " + countryInRussian.upper() + " сказки с адреса: " + countryUrl + "\n")

        slave_request = requests.get(countryUrl)
        slave_soup = BeautifulSoup(slave_request.text, "lxml")

        for tale in slave_soup.findAll("div", {"class": "left_div"}):

            try:
                print("raz", str(tale))
                taleInfo = str(tale)[82:]
                print("dva", taleInfo)
                taleInfo = taleInfo.split('"')[0]
                print("tri", taleInfo)
                taleInfo = taleInfo.split('/')[2]

                print(taleInfo)
                print(ourURL + taleInfo)
                fileName = our_dir + countryInRussian + "/" + taleInfo + ".txt"
                print(fileName)
                print("\n")

                tale_url = ourURL + taleInfo
                tale_request = requests.get(tale_url)
                tale_soup = BeautifulSoup(tale_request.content, "lxml")

                urlKey = re.findall("\d+", str(taleInfo))[0]
                taleBody = tale_soup.find("div", id="news-id-" + urlKey)
                os.makedirs(os.path.dirname(fileName), exist_ok=True)
                with open(fileName, "w", encoding = "utf-8") as f:

                    dirty_text = str(taleBody)
                    pattern1 = r"< p >"
                    pattern2 = r"<br/>"
                    pattern3 = r"<.+>"
                    after_pattern1 = re.sub(pattern1, "\n", dirty_text)
                    after_pattern2 = re.sub(pattern2, "\n", after_pattern1)
                    after_pattern3 = re.sub(pattern3, "", after_pattern2)
                    clean_text = after_pattern3
                    f.write(clean_text)

            except IndexError: # эта ошибка возникает для подкаталогов сказок
                print("Error!")

talesLoader()

# http://stackoverflow.com/a/3947323
for root, _, files in os.walk(our_dir): # удалим файлы с содержимым "None" после ошибки подкаталогов
    for f in files:
        fullpath = os.path.join(root, f)
        if os.path.getsize(fullpath) < 30:
            os.remove(fullpath)
            print("БЫЛ УДАЛЁН ФАЙЛ: " + root[len(our_dir):] + "/" + f)
