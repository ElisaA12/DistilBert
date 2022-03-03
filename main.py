import spacy
from question_processor import QuestionProcessor
from text_extractor import TextExtractor
from context_retriever import ContextRetriever
from answer_retriever import AnswerRetriever
import wikipedia

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

while True:
    originalQuestion = input('Insert the question:').lower()
    if lingua == 'it':
        textExtractor1 = TextExtractor(namePage, "it", contesto)
        # inizializzo la funzione nlp della lingua italiana
        nlp = spacy.load("it_core_news_sm")  # md
    else:
        textExtractor1 = TextExtractor(namePage, "en", contesto)
        # inizializzo la funzione nlp della lingua inglese.
        nlp = spacy.load("en_core_web_sm")  # md

    textExtractor1.extract()
    # textExtractorPipe = TextExtractorPipe()

    nlp.add_pipe('sentencizer')
    # doc = nlp(textExtractorPipe.extract())
    doc = nlp(textExtractor1.search())
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
