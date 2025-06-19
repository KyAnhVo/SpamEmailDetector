from typing import Tuple, List, Dict

from nltk.corpus import stopwords
import nltk
import NB
import re
import heapq

class SpamVocabulary:
    emails: List[List[str | bool]]
    vocabulary: Dict[str, int]
    activeVocabulary: Dict[str, int]
    activeVocabularySize: int
    activeVocabularyUpdated: bool

    def __init__(self, emails: List[List[str | bool]], activeVocabularySize: int = 300):
        self._ensureStopword()

        self.emails = emails
        self.activeVocabularySize = activeVocabularySize
        self._fillVocabulary()
        self._updateActiveVocabulary()
    
    def _tokenize(self, string: str) -> List[str]:
        lowered = string.lower()
        return re.findall(r'\b[a-z]+\b', lowered)
    
    def _fillVocabulary(self):
        self.vocabulary = {}
        stopwordSet = set(stopwords.words('english'))
        stopwordSet.add('subject')
        for email, _ in self.emails:
            words = self._tokenize(email)
            for word in words:
                if word in stopwordSet:
                    continue
                self.vocabulary[word] = self.vocabulary.get(word, 0) + 1
    
    def _updateActiveVocabulary(self):
        assert(self.vocabulary is not None), 'vocabulary is not instantiated'
        mostAppeared = heapq.nlargest(
            n= self.activeVocabularySize, 
            iterable= self.vocabulary.items(), 
            key= lambda x: x[1])
        self.activeVocabulary = {item[0]: item[1] for item in mostAppeared}
        self.activeVocabularyUpdated = True
    
    def addEmail(self, email: str, isSpam: bool):
        self.emails.append([email, isSpam])
        words = self._tokenize(email)

        # Change vocabulary
        for word in words:
            if word in stopwords.words('english'):
                continue
            self.vocabulary[word] = self.vocabulary.get(word, 0) + 1
        
        self.activeVocabularyUpdated = False

    def flagEmail(self, email: str, isSpam: bool):
        for i, (content, _) in enumerate(self.emails):
            if content == email:
                self.emails[i][1] = isSpam
                return
        raise ValueError('email not in email list')
    
    def _ensureStopword(self) -> None:
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet= True)

emails = [['Subject: I am Lebron the Second', True], ['Subject: I am the Hulk', False]]
vocab = SpamVocabulary(emails, 2)
print(vocab.emails)
print(vocab.vocabulary)
print(vocab.activeVocabulary)
