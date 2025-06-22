import sys
import os
import csv
import ctypes

import tkinter as tk
from tkinter import filedialog

import torch

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
    
def getFile() -> str:
    root = tk.Tk()
    root.withdraw()
    filepath: str = filedialog.askopenfilename()
    return filepath

def main():
    CSV_FILE: str = os.getcwd() + '/emails.csv'
    ACTIVE_VOCAB_COUNT: int = 1000

    emailList: SedVocabulary = buildEmailList(file= CSV_FILE, activeVocabCount= ACTIVE_VOCAB_COUNT)
    x, y = emailList.getInputLst()
    x, y = torch.tensor(x), torch.tensor(y)

    predictor: NB = NB(x, y, 2)

    while True:
        if not input('Get email prediction? (Y|n)').lower() == 'y':
            break
        filename = getFile()
        
        email = ''
        with open(file= filename, mode= 'r', encoding= 'utf-8') as emailFile:
            email = emailFile.read()
        
        print(predictor.predict(
            torch.tensor(emailList.emailToList(email), dtype= torch.float32, device= 'cuda' if torch.cuda.is_available() else 'cpu')
        ))


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    main()