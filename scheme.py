import abc
from turtle import write_docstringdict
from typing import List, Type


def create_tagger(scheme):
    if scheme == 'IOB2':
        return IOB2Tagger()
    else:
        raise ValueError(f"The scheme value is invalid: {scheme}")


class BaseTagger(abc.ABC):
    @abc.abstractmethod
    def tag(self, words: List[str], label: str):
        assert len(words) > 0


class IOB2Tagger(BaseTagger):
    def tag(self, words: List[str], label: str, origin: str):
        super().tag(words, label)
        if label=='O':
            return [f"O"]* len(words)
        elif origin=='I':
            return [f"I-{label}"] * len(words)
        elif origin=='B':
            return [f"B-{label}"] + [f"I-{label}"] * (len(words) - 1)


