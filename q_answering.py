import spacy
from rank_bm25 import BM25Okapi
import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
from text_extractor import TextExtractor
from text_extractor_pipe import TextExtractorPipe

from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


class QA:

    # Initialization of the class
    def __init__(self):
        self.nlp = nlp = spacy.load("en_core_web_sm")
        return

    def process(self, text):
        pos = ["NOUN", "PROPN", "ADJ"]
        tokens = self.nlp(text)
        return ' '.join(token.text for token in tokens if token.pos_ in pos)

    # FILE 2
    # SORT DOCUMENTS ACCORDING TO QUESTION
    def tokenize(self, sentence):
        return [token.lemma_ for token in self.nlp(sentence)]

    def getContext(self, sentences, question, numberOfResults=10):
        documents = []
        for sent in sentences:
            documents.append(self.tokenize(sent))
        print(documents)
        bm25 = BM25Okapi(documents)

        scores = bm25.get_scores(self.tokenize(question))
        results = {}
        for index, score in enumerate(scores):
            results[index] = score

        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        results_list = list(sorted_results.keys())
        final_results = results_list if len(results_list) < numberOfResults else results_list[:numberOfResults]
        questionContext = ""
        for final_result in final_results:
            questionContext = questionContext + " ".join(documents[final_result])
        return questionContext

    # FILE3
    def find_answer(self, question, questionContext):

        distilBertTokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True)

        distilBertForQuestionAnswering = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        '''
        encodings = distilBertTokenizer.encode_plus(question, questionContext)

        inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]

        scoresStart, scoresEnd = distilBertForQuestionAnswering(torch.tensor([inputIds]), attention_mask=torch.tensor([attentionMask]))
        '''
        inputs = distilBertTokenizer(question, questionContext, return_tensors='pt')

        start_positions = torch.tensor([1])
        end_positions = torch.tensor([3])

        outputs = distilBertForQuestionAnswering(**inputs, start_positions=start_positions, end_positions=end_positions)
        loss = outputs.loss
        scoresStart = outputs.start_logits
        scoresEnd = outputs.end_logits

        encodings = distilBertTokenizer.encode_plus(question, questionContext)

        inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]

        tokens = inputIds[torch.argmax(scoresStart): torch.argmax(scoresEnd) + 1]

        answerTokens = distilBertTokenizer.convert_ids_to_tokens(tokens, skip_special_tokens=True)

        results = distilBertTokenizer.convert_tokens_to_string(answerTokens)

        return results

    # Get answer
    def get_answer(self, question):

        textExtractor1 = TextExtractor("Berlin", "Q64")
        textExtractor1.extract()

        textExtractorPipe = TextExtractorPipe()
        textExtractorPipe.addTextExtractor(textExtractor1)
        print(textExtractorPipe)
        self.nlp.add_pipe('sentencizer')
        doc = self.nlp(textExtractorPipe.extract())
        #print(doc)
        sentences = [sent.text.strip() for sent in doc.sents]
        sentences = [string for string in sentences if string != ""]
        #print(sentences)
        questionContext = self.getContext(sentences, self.process(question))

        print(question)

        answer = self.find_answer(question, questionContext)

        return answer

