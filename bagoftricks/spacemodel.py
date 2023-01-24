"""
A class implementing a simple model for estimating whether a token is followed by a
space or not based. Useful for normalizing datasets on the form:

```python
sample = {"tokens": ["This", "is", "a", "sample", ".", "Without", "spaces", ".", "It", "'",
          "s", "a", "problem", "."],
          labels: ["label", "label", "label", "label", "label" ,"label", "label", "label", "label", "label",
          "label", "label", "label"]  
}
```

to its sentence form

requires:
    spacy
    (datasets)
"""

from collections import defaultdict
from typing import Iterable

import spacy
import tqdm
from spacy.tokens import Doc


class SpaceModel:
    """
    Attributes:
        followed_by_space_diff (Dict[str, int]): The difference in the number of times a
            word is followed by a space and not. I.e.
            {Number of times followed by space}-{Number of times not followed by space}

    """

    def __init__(self, lang: str):
        self.followed_by_space_diff = defaultdict(int)
        self.preceded_by_space_diff = defaultdict(int)

        self.nlp = spacy.blank(lang)

    def fit(self, texts: Iterable[str], **kwargs) -> None:
        self.reset()

        docs = self.nlp.pipe(texts, **kwargs)
        for doc in tqdm.tqdm(docs):
            self.update(doc)

    def reset(self) -> None:
        self.followed_by_space_diff = defaultdict(int)
        self.preceded_by_space_diff = defaultdict(int)

    def update(self, doc: Doc) -> None:
        for prev_tok, tok in zip(doc, doc[1:]):  # skips the last token
            self.followed_by_space_diff[tok.text] += 1 if tok.whitespace_ else -1
            self.preceded_by_space_diff[tok.text] += 1 if prev_tok.whitespace_ else -1

    def followed_by_space(self, tokens: list[str]) -> list[bool]:
        """
        from a list of tokens produce an array of a boolean array of whether the
        specific word is followed by a space.
        """
        doc = Doc(self.nlp.vocab, words=tokens)
        return self.__followed_by_space_doc(doc)

    def __followed_by_space_doc(self, doc: Doc) -> list[bool]:
        max_len = len(doc) - 1
        followed_by_space = []
        for t in doc:
            diff = self.followed_by_space_diff[t.text]
            if t.i < max_len:
                next_tok = doc[t.i + 1]
                diff += self.preceded_by_space_diff[next_tok.text]
            token_followed_by_space = diff >= 0
            followed_by_space.append(token_followed_by_space)
        return followed_by_space


## --- Utility ------------------------------------------


def load_books():
    from books import flatland, oliver_twist, secret_garden

    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    docs = nlp.pipe([oliver_twist, flatland, secret_garden])

    # split into sentences of three
    sents = [sent for doc in docs for sent in doc.sents]
    n = 3
    blocks = [sents[i : i + n] for i in range(0, len(sents), n)]
    three_sents_spans = [s[0].doc[s[0].start : s[-1].end] for s in blocks]

    return [span.text for span in three_sents_spans]


def load_texts(lang: str, n_docs: int) -> list[str]:
    # untested due to services being down?!
    from datasets import load_dataset

    ds = load_dataset(
        "oscar", f"unshuffled_deduplicated_{lang}", streaming=True, split="train"
    )
    data_stream = iter(ds)
    return [next(data_stream)["text"] for i in range(n_docs)]


if __name__ == "__main__":
    model = SpaceModel(lang="en")
    model.fit(load_books())

    tokens = [
        "This",
        "is",
        "a",
        "sample",
        ".",
        "Without",
        "spaces",
        ".",
        "It",
        "'",
        "s",
        "a",
        "problem",
        ".",
        "Speaker",
        "1",
        ":",
        "say",
        "cheese",
        "!",
    ]

    # overwrite (probably not enough training data)
    model.followed_by_space_diff["."] = 20
    next_is_space = model.followed_by_space(tokens)

    doc = Doc(model.nlp.vocab, words=tokens, spaces=next_is_space)
    print(doc)

    model.fit(load_texts("da", 10_000))
    next_is_space = model.followed_by_space(tokens)

    doc = Doc(model.nlp.vocab, words=tokens, spaces=next_is_space)
    print(doc)