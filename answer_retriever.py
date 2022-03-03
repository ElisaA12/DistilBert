import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
from transformers import pipeline

model_name_Bertino = "dbmdz/bert-base-italian-uncased"


class AnswerRetriever:

    def getAnswer(self, question, questionContext, lingua):
        if lingua=='en':
            distilBertTokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True)
            distilBertForQuestionAnswering = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        else:
            #per la versione italiana utilizziamo un modello che e' la versione italiana del BERT
            questionAnswering = pipeline('question-answering', model='antoniocappiello/bert-base-italian-uncased-squad-it') #ritorna le score
            out = questionAnswering(context=questionContext, question=question)
            return out['answer']

        #se abbiamo scelto la versione inglese continuiamo con il codice base
        inputs = distilBertTokenizer(question, questionContext, return_tensors='pt')
        start_positions = torch.tensor([1])
        end_positions = torch.tensor([3])

        outputs = distilBertForQuestionAnswering(**inputs, start_positions=start_positions, end_positions=end_positions)

        scoresStart = outputs.start_logits
        scoresEnd = outputs.end_logits

        encodings = distilBertTokenizer.encode_plus(question, questionContext)

        inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]

        tokens = inputIds[torch.argmax(scoresStart): torch.argmax(scoresEnd) + 1]

        answerTokens = distilBertTokenizer.convert_ids_to_tokens(tokens, skip_special_tokens=True)
        #print("anstokens \n", answerTokens)
        return distilBertTokenizer.convert_tokens_to_string(answerTokens)

