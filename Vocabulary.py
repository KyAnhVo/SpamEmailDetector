from typing import Tuple, List, Dict

from nltk.corpus import stopwords
import NB
import re
import heapq

class SpamVocabulary:
    emails: List[Tuple[str, bool]]
    vocabulary: Dict[str, int]
    activeVocabulary: Dict[str, int]
    activeVocabularySize: int

    def __init__(self, emails: List[Tuple[str, int]], activeVocabularySize: int = 1000):
        self.emails = emails
        self.activeVocabularySize = activeVocabularySize
        self._fillVocabulary()
        self._fillActiveVocabulary()

    
    def _tokenize(self, string: str) -> List[str]:
        lowered = string.lower()
        return re.findall(r'\b[a-z]+\b', lowered)
    
    def _fillVocabulary(self):
        self.vocabulary = {}
        for email, isSpam in self.emails:
            words = self._tokenize(email)
            for word in words:
                self.vocabulary[word] = self.vocabulary.get(word, 0) + 1
    
    # TODO: Optimize this function (currently O(n log n))
    def _fillActiveVocabulary(self):
        assert(self.vocabulary is not None), 'vocabulary is not instantiated'
        mostAppeared = heapq.nlargest(
            n= self.activeVocabularySize, 
            iterable= self.vocabulary.items(), 
            key= lambda x: x[1])
        self.activeVocabulary = {word: appearance for word, appearance in mostAppeared}