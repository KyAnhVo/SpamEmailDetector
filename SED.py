import sys
import os
import csv

from typing import List, Tuple, Dict

from NB import NB
from Vocabulary import SedVocabulary

def buildEmailList(file: str, activeVocabCount: int) -> SedVocabulary:
    emails: List[list[str, bool]]  = []
    with open(file, 'r', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)

        for row in csvReader:
            isSpam = (row[0] == 'spam')
            email = row[1]
            emails.append([email, isSpam])
        
        return SedVocabulary(emails, activeVocabularySize= activeVocabCount)

def main():
    CSV_FILE: str = os.getcwd() + 'emails.csv'
    ACTIVE_VOCAB_COUNT: int = 1000

    nbObject: NB = NB()
    emailList: SedVocabulary = buildEmailList(file= CSV_FILE, activeVocabCount= ACTIVE_VOCAB_COUNT)

    

