from spacy.tokens import Doc

from nltk.tokenize import RegexpTokenizer


class NLTKTokenizer:
    """
    The NLTK tokenizer is noticeably faster than the spacy tokenizer
    though performs notably worse tokenization:

    Speed Comparison on a text of 237 tokens:

    multiplication factor: time

    NLTK
    10: 0.004389047622680664
    100: 0.018768787384033203
    1000: 0.17305397987365723
    10000: 1.4743471145629883
    SPACY
    10: 0.019192934036254883
    100: 0.15356707572937012
    1000: 1.7956039905548096
    10000: 18.097763776779175

    Example:
        >>> nlp = spacy.blank("en")
        >>> nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)
        >>> doc = nlp("What's happened to me? he thought. It wasn't a dream.")
    """

    def __init__(self, vocab):
        self.vocab = vocab
        self.tokenizer = RegexpTokenizer("\s+", gaps=True)

    def __call__(self, text):
        words = self.tokenizer.tokenize(text)
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)
