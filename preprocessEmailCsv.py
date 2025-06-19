import csv

seperate = '\n' + ('#' * 20) + '\n'
csvLst = []

with open('esd/spam_ham_dataset.csv', 'r') as file:
    csvReader = csv.reader(file, delimiter= ',')
    read = False
    for row in csvReader:
        if not read:
            read = True
            continue
        email = row[2]
        isSpam = row[1]
        csvLst.append([isSpam, email])

with open('esd/modified.csv', 'w', encoding= 'utf-8', newline='') as file:
    writer = csv.writer(file, delimiter= ',', quoting= csv.QUOTE_ALL)
    writer.writerows(csvLst)