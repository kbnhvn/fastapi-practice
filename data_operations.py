import csv
from typing import List

### ---- Lecture/Ecriture données CSV ---- ###

#Lecture des données CSV
def load_csv_data(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

#Ecriture des données dans le fichier CSV
def add_data_to_csv(file_path, question):
    with open(file_path, mode='a', newline='') as file:
        fieldnames=['question', 'subject', 'use', 'correct', 'responseA', 'responseB', 'responseC', 'responseD', 'remark']
        # fieldnames = question.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(question.dict())

### ---- Recherche/Filtre de données ---- ###
"""
Ces fonctions permettent de filtrer et retourner les données contenues dans un tableau.
Ce tableau est obtenu grâce à la fonction load_csv_data() ci-dessus.
"""

#Retourne les différentes valeurs (uniques) de types de QCM 
def filter_uses(list: List):
    return set(element.get('use') for element in list)

#Retourne  les différentes valeurs (uniques) de catégories pour un type donné
def filter_subjects_by_use(list: List, use: str):
    list_subjects = []
    for element in list:
        if element['use'] == use:
            list_subjects.append(element)
    return set(element.get('subject') for element in list_subjects)

#Retourne les questions pour le type donné
def filter_questions_by_use(list: List, use: str):
    list_questions=[]
    for element in list:
        if element['use'] == use:
            list_questions.append(element)
    return list_questions   

#Retourne les questions pour les catégories données
def filter_questions_by_subjects(list: List, subjects: List):
    list_questions=[]
    for element in list:
        if element['subject'] in subjects:
            list_questions.append(element)
    return list_questions



