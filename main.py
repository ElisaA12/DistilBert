import spacy
from question_processor import QuestionProcessor
from text_extractor import TextExtractor
from context_retriever import ContextRetriever
from answer_retriever import AnswerRetriever
import wikipedia
import os

lingua = input('Insert the language you want [en , it]:')

wikipedia.set_lang(lingua)
page = input('Insert the name of the page:')

search = wikipedia.search(page, results=15, suggestion=False)
print(search)
id = input('Select the number of the page you want:')
id = int(id)
print(search[id])
namePage = search[id]
contesto = input('Do you want research in the table or in the text? [table , text]: ')

os.chdir('./Desktop/DistilBert-main')

while True:
    originalQuestion = input('Insert the question:').lower()
    if lingua == 'it':
        textExtractor = TextExtractor(namePage, "it", contesto)
        # inizializzo la funzione nlp della lingua italiana
        
        try:
            spacy.load("it_core_news_sm")  # md
        except:
            print("Installazione lingua italiana ")
            os.system("python -m spacy download it_core_news_sm")
        nlp = spacy.load("it_core_news_sm")  # md
    '''
    else:
        textExtractor = TextExtractor(namePage, "en", contesto)
        # inizializzo la funzione nlp della lingua inglese.
        try:
            spacy.load("en_core_web_sm")  # md
        except:
            print("English leanguage download")
            os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")  # md
    '''


    textExtractor.extract()
    #Aggiunge un componente alla pipeline di elaborazione.
    nlp.add_pipe('sentencizer')
    doc = nlp(textExtractor.search())

    #itera le frasi in un documenti eliminando il primo e l'ultim carettere
    sentences = [sent.text.strip() for sent in doc.sents]
    sentences = [string for string in sentences if string != ""]
    questionProcessor = QuestionProcessor(nlp)
    contextRetriever = ContextRetriever(nlp, 10)
    answerRetriever = AnswerRetriever()

    questionContext = contextRetriever.getContext(sentences, questionProcessor.process(originalQuestion))
    answer = answerRetriever.getAnswer(originalQuestion, questionContext, lingua)
    print("\nrisposta:  ", answer)

    another = input('\nDo you want ask another question? [yes , no]: ')
    if another.lower() == "no":
        break
