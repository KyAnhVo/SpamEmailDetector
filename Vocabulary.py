from typing import Tuple, List, Dict, Set

from nltk.corpus import stopwords
import nltk
import NB
import re
import heapq
import copy

class SedVocabulary:
    emails: List[list[str, bool]]
    vocabulary: Dict[str, int]
    _activeVocabulary: Dict[str, int]
    activeVocabularySize: int
    activeVocabularyUpdated: bool
    stopwordSet: Set

    def __init__(self, emails: List[List[str | bool]], activeVocabularySize: int = 300):
        self._ensureStopword()

        self.emails = emails
        self.activeVocabularySize = activeVocabularySize

        self.stopwordSet = set(stopwords.words('english'))
        self.stopwordSet.add('subject')

        self._fillVocabulary()
        self._updateActiveVocabulary()
    
    def getActiveVocabulary(self) -> Dict[str, int]:
        if not self.activeVocabularyUpdated:
            self._updateActiveVocabulary()
        return self._activeVocabulary

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
    
    def getInputLst(self) -> Tuple[List[List[int]], List[int], List[str]]:
        if not self.activeVocabularyUpdated:
            self._updateActiveVocabulary()

        inputLst = sorted(list(self._activeVocabulary.keys()))
        indexDict = {string: index for index, string in enumerate(inputLst)}

        x = [[0 for i in range(len(inputLst))] for j in range(len(self.emails))]
        y = []

        for i, (email, isSpam) in enumerate(self.emails):
            
            # handle x 
            words = self._tokenize(email)
            for word in words:
                if word not in indexDict:
                    continue
                x[i][indexDict[word]] = 1
            
            # handle y
            y.append(int(isSpam))
        
        return x, y, inputLst
    
    def _tokenize(self, string: str) -> List[str]:
        lowered = string.lower()
        return re.findall(r'\b[a-z]+\b', lowered)
    
    def _fillVocabulary(self):
        self.vocabulary = {}
        for email, _ in self.emails:
            words = self._tokenize(email)
            for word in words:
                if word in self.stopwordSet:
                    continue
                self.vocabulary[word] = self.vocabulary.get(word, 0) + 1
    
    def _updateActiveVocabulary(self):
        assert(self.vocabulary is not None), 'vocabulary is not instantiated'
        mostAppeared = heapq.nlargest(
            n= self.activeVocabularySize, 
            iterable= self.vocabulary.items(), 
            key= lambda x: x[1])
        self._activeVocabulary = {item[0]: item[1] for item in mostAppeared}
        self.activeVocabularyUpdated = True
    
    def _ensureStopword(self) -> None:
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet= True)