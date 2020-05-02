#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:37:31 2020

@author: wally
"""

import pandas as pd
from math import sqrt
import csv

def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
        return dataset

train_data = load_csv("./training.csv")
test_data = load_csv("./testing.csv")

def distance(X1, X2):
    sum = 0.0
    for i in range (len(X2)):
        sum += (float(X1[i]) - float(X2[i])) * (float(X1[i]) - float(X2[i]))
    return sqrt(sum)

def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

def get_neighbors(train, test, k):
    distances = list()
    for row in train:
        dist = distance(row, test)
        distances.append((row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for neighbor in range(k):
        neighbors.append(distances[neighbor][0])
    return neighbors

def prediction_classification(train, test, k):
    neighbors = get_neighbors(train, test, k)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction

def KNN(train, test, k):
    predictions = list()
    for row in test:
        predictions.append((row, prediction_classification(train, row, k)))
    return predictions

k = 3

pd.options.display.max_colwidth = 1000
questions = pd.read_csv('./questions.csv', sep=';'  , engine='python')
name = input("Seu nome é? ")
answers = list()
for index, row in questions.iterrows():
    print(row)
    answer = "0"
    while answer not in ["1", "2", "3", "4"]:
        answer = input("\nDigite o número de sua resposta: ")
        if answer not in ["1", "2", "3", "4"]:
            print("\nResposta inválida! Selecione uma opção de 1 a 4!\n")
    answers.append(float(answer))
print(answers)
print("\nKNN Seletor: Difícil. Muito difícil. Tem muita coragem, estou vendo. Uma mente nada má também.\n Tem talento, se tem. E uma sede de provar seu valor. \nMas onde vou colocá-lo?")
label = prediction_classification(train_data, answers, k)
str_column_to_int(train_data, len(train_data[0])-1)
print("\nKNN Seletor: Não? Tem certeza? \nVocê poderia ser grande, sabia? Está tudo aqui, na sua cabeça. \nE iria ajudá-lo a alcançar essa grandeza. Não há dúvida sobre isso. Não?")
print("\nBom, se tem certeza... é melhor que seja...\n")
print('\nA partir de hoje você se chamará %s de %s' % (name, label))