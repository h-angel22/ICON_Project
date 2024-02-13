# learnCrossValidation.py - Cross Validation for Parameter Tuning
# AIFCA Python code Version 0.9.12 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2023 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import os
from learnProblem import Data_set, Data_from_file, Evaluate
from learnNoInputs import Predict
from learnDT import DT_learner
import matplotlib.pyplot as plt
import random

class K_fold_dataset(object):
    def __init__(self, training_set, num_folds):
        self.data = training_set.train.copy()
        self.target = training_set.target
        self.input_features = training_set.input_features
        self.num_folds = num_folds
        self.conditions = training_set.conditions

        random.shuffle(self.data)
        self.fold_boundaries = [(len(self.data)*i)//num_folds
                                for i in range(0,num_folds+1)]

    def fold(self, fold_num):
        for i in range(self.fold_boundaries[fold_num],
                       self.fold_boundaries[fold_num+1]):
            yield self.data[i]

    def fold_complement(self, fold_num):
        for i in range(0,self.fold_boundaries[fold_num]):
            yield self.data[i]
        for i in range(self.fold_boundaries[fold_num+1],len(self.data)):
            yield self.data[i]

    def validation_error(self, learner, error_measure, **other_params):
        error = 0
        try:
            for i in range(self.num_folds):
                predictor = learner(self, train=list(self.fold_complement(i)),
                                    **other_params).learn()
                error += sum( error_measure(predictor(e), self.target(e))
                              for e in self.fold(i))
        except ValueError:
            return float("inf")  #infinity
        return error/len(self.data)

def check_error(data, criterion=Evaluate.squared_loss, leaf_prediction=Predict.empirical, num_folds=5, maxx=None):
    folded_data = K_fold_dataset(data, num_folds)
    if maxx == None:
        maxx = len(data.train)//2+1

    verrors = []
    for mcw in range(1,maxx):
        verrors.append(folded_data.validation_error(DT_learner,criterion,leaf_prediction=leaf_prediction, min_child_weight=mcw))
        
    return verrors

absolute_path = os.path.dirname(__file__)
relative_path = "./data/bossfight.csv"
full_path = os.path.join(absolute_path, relative_path)
data = Data_from_file(full_path, separator=',', target_index=-1)
accuracy_array = check_error(data, criterion=Evaluate.accuracy, maxx=11)

print(accuracy_array)