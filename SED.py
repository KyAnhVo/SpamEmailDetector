import sys
import os
import csv

from NB import NB
from Vocabulary import SedVocabulary

CSV_FILE = os.getcwd() + 'emails.csv'

nbObject = NB()

def buildEmailList(file: str, activeVocabCount: int) -> SedVocabulary:
    emails = []
    with open(file, 'r', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)

        for row in csvReader:
            isSpam = (row[0] == 'spam')
            email = row[1]
            emails.append([email, isSpam])
        
        return SedVocabulary(emails, activeVocabularySize= activeVocabCount)