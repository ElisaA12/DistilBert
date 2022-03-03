import wikipedia
import os
import io
import re
from bs4 import \
    BeautifulSoup  # nell’estrazione di informazioni da una pagina web in maniera automatizzata. web scraping.
from urllib import \
    request  # Il modulo urllib.request fornisce una API per utilizzare le risorse Internet identificate da URL.


class TextExtractor:
    __pageTitle: str
    __pageLang: str

    def __init__(self, pageTitle, pageLang, contesto):
        self.__pageTitle = pageTitle
        self.__pageLang = pageLang
        self.__contesto = contesto

    def extract(self):
        fileName = "./text/" + self.__pageTitle + ".txt"

        if not os.path.isfile(fileName):
            f = io.open(fileName, "w", encoding="utf-8")

            source = request.urlopen(wikipedia.page(
                self.__pageTitle).url).read()  # Si passi un URL a urlopen() per ottenere un handle "tipo file" dei dati remoti.

            soup = BeautifulSoup(source, 'lxml')
            final = ""
            # le tabelle a seconda se la pagina e' in inglese o in italiano avranno classe diversa
            if (self.__pageLang == "it"):
                sections = soup.find("table", {"class": "sinottico"})
            else:
                sections = soup.find("table", {"class": "infobox geography vcard"})

            '''vado a prendere tutti i tag figli del tag <table>.
            se e' th: vado solamente a prendere il testo
            se e' td: vado a lavorare sugli spazi, altrimenti mi riportera' le parole tutte vicine
            vado anche a lavorare sui numeri, che controllero' con  (any(map(str.isdigit, words)))
            ovvero voglio che se ho due numeri separati da spazio, voglio togliere tale spazio.
            '''
            children = sections.findChildren()
            for child in children:
                if (child.name == "th"):
                    final = final + child.get_text() + " "
                if (child.name == "td" ):
                    if re.search(r'\d', child.get_text()):
                        list = child.get_text().split()
                        lista = ""
                        lista_tot = ""
                        for words in list:
                            if (any(map(str.isdigit, words))):
                                lista_tot = lista_tot + words
                                lista = ""
                            else:
                                lista = lista + " " + words
                                lista_tot = lista_tot + lista   + " "

                                lista = ""
                        final = final + lista_tot
                        if(self.__pageLang=="it"):
                            final = final + " "
                        else:
                            final = final +". "
                    else:
                        final = final + child.get_text() + " "

            page = wikipedia.page(title=self.__pageTitle)  # pageid=self.__pageId
            f.write(self.__pageLang + "\n" + final + "\n" + "table" + "\n" + page.content)

            f.close()

    def search(self) -> str:
        f = open("./text/" + self.__pageTitle + ".txt", "r", encoding="utf-8")
        text = ""
        if (self.__contesto == "table"):
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                if (line == "table"):
                    return text
                text += line
        else:
            lines = f.readlines()
            tab=True
            for line in lines:
                line = line.rstrip()
                if (line == "table"):
                    tab=False
                    line = line.rstrip()
                if(tab==False):
                    text += line
            return text

    def getText(self):
        f = open("./text/" + self.__pageTitle + ".txt", "r", encoding="utf-8")
        return f.read()
