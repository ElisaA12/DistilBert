from rank_bm25 import BM25Okapi


class ContextRetriever:

    def __init__(self, nlp, numberOfResults):
        self.nlp = nlp
        self.numberOfResults = numberOfResults

    def tokenize(self, sentence):
        return [token.lemma_ for token in self.nlp(sentence)]

    def getContext(self, sentences, question):
        documents = []
        for sent in sentences:
            documents.append(self.tokenize(sent))

        '''nella libreria gensim il metodo summarization.bm25 e' ormai deprecato. Ne ovviamo sostituendolo con
        la libreria rank-bm25 che e' na raccolta di algoritmi per interrogare una serie di documenti e restituire 
        quelli più rilevanti per la query. Andremo in particolare ad usare la funzione Okapi BM25 
        '''
        bm25 = BM25Okapi(documents)
        scores = bm25.get_scores(self.tokenize(question))
        results = {}
        for index, score in enumerate(scores):
            results[index] = score

        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        results_list = list(sorted_results.keys())
        final_results = results_list if len(results_list) < self.numberOfResults else results_list[
                                                                                      :self.numberOfResults]
        questionContext = ""
        for final_result in final_results:
            questionContext = questionContext + " ".join(documents[final_result])

        #print("context che cerco\n",questionContext)
        questionContext = questionContext.lower()
        return questionContext
