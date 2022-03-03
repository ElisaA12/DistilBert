class QuestionProcessor:

    def __init__(self, nlp):
        self.pos = ["NOUN", "PROPN", "ADJ"]
        self.nlp = nlp

    def process(self, text):
        tokens = self.nlp(text)
        return ' '.join(token.text for token in tokens if token.pos_ in self.pos)
