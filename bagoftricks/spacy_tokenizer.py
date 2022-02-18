from spacy.tokens import Doc

from nltk.tokenize import RegexpTokenizer


class NLTKTokenizer:
    """
    The NLTK tokenizer is noticeably faster than the spacy tokenizer
    though performs notably worse tokenization:

    Speed Comparison on a text of 237 tokens:

    .. code:

        text multiplication: time taken to tokenize

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

    Note this removes newlines and does not keep the text intact. Therefore it sets
    the extension: doc._.text to keep the original text.

    Example:
        >>> nlp = spacy.blank("en")
        >>> nlp.tokenizer = NLTKTokenizer(nlp.vocab)
        >>> doc = nlp("What's happened to me? he thought. It wasn't a dream.")
    """

    def __init__(self, vocab):
        self.vocab = vocab
        self.tokenizer = RegexpTokenizer(pattern=r"\w+|[^\w\s]+")

        if not Doc.has_extension("text"):
            Doc.set_extension("text", default=None)

    def __call__(self, text):
        words = self.tokenizer.tokenize(text)
        doc = Doc(self.vocab, words=words)
        doc._.text = text
        return doc


if __name__ == "__main__":
    text = """Samling af 3 forskellige korpusser: korpus90, korpus2000, korpus2010
    (bemærkning: De dækker hver især årene rundt om 90, 2000 og 2010 (og selve året))
    POS-tagget og lemmatiseret.

    KODE-DSL-LICENS: Hvis du vil bruge KorpusDK, skal du først sende en anmodning om et
    kodeord per e-mail til korpus@dsl.dk. Anmodningen skal indeholde en beskrivelse af
    det eller de formål, du påtænker at bruge korpusset til. I din anmodning skal du
    desuden erklære, at du accepterer og vil overholde en række brugsbetingelser.
    
    Vi bruger cookies til at tilpasse vores indhold og annoncer, til at vise dig
    funktioner til sociale medier og til at analysere vores trafik. Vi deler også
    oplysninger om din brug af vores hjemmeside med vores partnere inden for sociale
    medier, annonceringspartnere og analysepartnere. Vores partnere kan kombinere disse
    data med andre oplysninger, du har givet dem, eller som de har indsamlet fra din
    brug af deres tjenester."""

    from spacy.tokenizer import Tokenizer
    import spacy
    import time

    def custom_tokenizer(nlp):  # very simple spacy tokenizer
        return Tokenizer(nlp.vocab)

    for t in [None, custom_tokenizer, NLTKTokenizer]:
        nlp = spacy.blank("da")
        if t:
            nlp.tokenizer = t(nlp)
        nlp.max_length = 500_000_000
        print(f"Tokenizer {t}")
        for i in [10, 100, 1000, 10000, 50000]:
            s = time.time()
            nlp(i * text)
            print(f"\t{i}\t{time.time()-s}")
