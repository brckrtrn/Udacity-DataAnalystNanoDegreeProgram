#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot
import pprint
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest

from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score
from numpy import mean
from sklearn import preprocessing


from sklearn.feature_selection import f_classif

from sklearn import grid_search
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from tester import test_classifier,dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### features_list
poi_label = ['poi']

financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                      'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                      'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                      'restricted_stock', 'director_fees']

email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages',
                  'from_this_person_to_poi', 'shared_receipt_with_poi']

#Concat all features
features_list = poi_label + financial_features + email_features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


##info

# Number of Person
#print "Number of Person : " + str(len(data_dict))

# POI and NON-POI count
poi_count = 0
for person in data_dict:
    if data_dict[person]['poi'] == True:
        poi_count += 1
print ('')
print ("Number of POI : ") + str(poi_count)
print ('')
print ("Number of NON-POI : ") + str((len(data_dict) - poi_count))


### Task 2: Remove outliers

### missing and non mising values find
print ("")
print ("Number of missing values in each feature: ")
nan_in_features = [0 for i in range(len(features_list))]
non_nan_in_features = [0 for i in range(len(features_list))]
for i, person in enumerate(data_dict.values()):
    for j, feature in enumerate(features_list):
        if person[feature] == 'NaN':
            nan_in_features[j] += 1
        if person[feature] != 'NaN' :
            non_nan_in_features[j] += 1

### missing values in each feature
for i, feature in enumerate(features_list):
    print (feature, nan_in_features[i])
print ("")

### non missing values in each feature
print ("Number of non missing values in each feature: ")

for i, feature in enumerate(features_list):
    print (feature, non_nan_in_features[i])
print ("")

### total missing values in each feature
total_nan_features_count = 0
for i, feature in enumerate(features_list):
    total_nan_features_count = total_nan_features_count + nan_in_features[i]
print ("Number of NaN values:", total_nan_features_count)
print ("")

### total non missing values in each feature
total_non_nan_features_count=0
for i, feature in enumerate(features_list):
    total_non_nan_features_count = total_non_nan_features_count + non_nan_in_features[i]
print ("Number of not NaN values:", total_non_nan_features_count)
print ("")

### total data point
total_features_count=0
for i, feature in enumerate(features_list):
    total_features_count = total_features_count + nan_in_features[i] + non_nan_in_features[i]
print ("Number of total data points:", total_features_count)
print ("")

##persons with a salary greater than $600K
print ("")
print ("persons with a salary greater than $600K:")
for l in data_dict:
    if data_dict[l]["salary"] != "NaN":
        if data_dict[l]["salary"] >= 600000:
            print (l)
print ("")

##persons with a bonus greater than $3M
print ("persons with a bonus greater than $3M:")
for l in data_dict:
    if data_dict[l]["bonus"] != "NaN":
        if data_dict[l]["bonus"] >= 3000000:
            print (l)
print ("")

#the largest salary
print ("and the largest salary goes to:")
i = 0
big_salary = "none"
for l in data_dict:
    if data_dict[l]["salary"] != "NaN":
        if data_dict[l]["salary"] > i:
            i = data_dict[l]["salary"]
            big_salary = l
print (big_salary)
print ("")

#the largest bonus
print ("and the largest bonus goes to:")
i = 0
big_bonus = "none"
for l in data_dict:
    if data_dict[l]["bonus"] != "NaN":
        if data_dict[l]["bonus"] > i:
            i = data_dict[l]["bonus"]
            big_bonus = l
print (big_bonus)
# total is obviously an outlier. IT will be removed

#the second largest salary
print ("and the second largest salary goes to:")
i = 0
big_salary = "none"
for l in data_dict:
    if data_dict[l]["salary"] != "NaN":
        if data_dict[l]["salary"] > i:
            i = data_dict[l]["salary"]
            big_salary = l
print (big_salary)
print ("")

#the second largest bonus
print ("and the second largest bonus goes to:")
i = 0
big_bonus = "none"
for l in data_dict:
    if data_dict[l]["bonus"] != "NaN":
        if data_dict[l]["bonus"] > i:
            i = data_dict[l]["bonus"]
            big_bonus = l
print (big_bonus)

#THE TRAVEL AGENCY IN THE PARK: this records does not represent a person .
#LOCKHART EUGENE E: This record does not contain any information.

print ("")
print ("THE TRAVEL AGENCY IN THE PARK and Eugene Lockhart have no entered data:")
print ("")
print (data_dict["THE TRAVEL AGENCY IN THE PARK"])
print ("")
print (data_dict["LOCKHART EUGENE E"])
print ("")

print ("")
print ("'Total' is obviously an outlier so we will remove it from the dataset")
print ("")
print ("We've decided to remove two entries more:")
print ("THE TRAVEL AGENCY IN THE PARK, and EUGENE LOCKHART")

#remove TOTAL, THE TRAVEL AGENCY IN THE PARK and LOCKHART EUGENE
data_dict.pop("TOTAL",0)
data_dict.pop("THE TRAVEL AGENCY IN THE PARK",0)
data_dict.pop("LOCKHART EUGENE E",0)


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

my_dataset = data_dict

#create new features, transformation of from_this_person_to_poi and from_poi_to_this_person values to ratios
for keys, values in data_dict.iteritems():
    if values["to_messages"] != "NaN" and \
       values["from_messages"] != "NaN" and \
       values["from_poi_to_this_person"] != "NaN" and \
       values["from_this_person_to_poi"] != "NaN":

       values["poi_to_person_rate"] = float(values["from_poi_to_this_person"]) / values["to_messages"]
       values["person_to_poi_rate"] = float(values["from_this_person_to_poi"]) / values["from_messages"]
    else:
       values["poi_to_person_rate"] = 0
       values["person_to_poi_rate"] = 0

#add new ones to features
features_list.extend (['poi_to_person_rate', 'person_to_poi_rate'])

print ("")
## Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

#Removes all but the k highest scoring features - after manually tries '7' is selected for k -

k = 7
selector = SelectKBest(f_classif, k=7)
selector.fit_transform(features, labels)
print("the score of each features:")

scores = zip(features_list[1:],selector.scores_)
sorted_scores = sorted(scores, key = lambda x: x[1], reverse=True)
pprint.pprint(sorted_scores)
optimized_features_list = poi_label + list(map(lambda x: x[0], sorted_scores))[0:k]

print(optimized_features_list)

#create new features list without new features
without_new_features_list =['poi', 'exercised_stock_options', 'total_stock_value', 'bonus',
                            'salary', 'deferred_income', 'long_term_incentive']

# Extract from dataset without new feature
data = featureFormat(my_dataset, without_new_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
scaler = preprocessing.MinMaxScaler()
features = scaler.fit_transform(features)

# Extract from dataset with new feature
data = featureFormat(my_dataset, without_new_features_list + [ 'poi_to_person_rate', 'person_to_poi_rate']
                     , sort_keys = True)
new_labels, new_features = targetFeatureSplit(data)
new_features = scaler.fit_transform(new_features)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point without new features. Try a variety of classifiers.

feature_train, feature_test, labels_train, labels_test = \
	train_test_split( features, labels, test_size=0.3, random_state=42)

# Provided to give you a starting point with new features. Try a variety of classifiers.
new_feature_train, new_feature_test, new_labels_train, new_labels_test = \
	train_test_split( new_features, new_labels, test_size=0.3, random_state=42)

print ("")

# best paramaters find
## tuning parmaters of SVM

SVM_clf = SVC()
s_param = {'kernel': ['rbf', 'linear', 'poly'], 'C': [ 0.1,1,10, 100, 1000],\
           'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 'random_state': [42]}
s_clf = grid_search.GridSearchCV(SVM_clf, s_param)
s_clf = s_clf.fit(features, labels)
s_clf = s_clf.best_estimator_

print (s_clf)

# best paramaters find
## tuning paramaters of Decision Trees

parameters = {'min_samples_leaf':[10,20,30,40,50], 'min_samples_split':[20,30,40,50]}

mclf = tree.DecisionTreeClassifier()
clf = grid_search.GridSearchCV(mclf, parameters)
clf = clf.fit(features, labels)
clf = clf.best_estimator_

print (clf)

print ("")

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

#Evaluate the models
def model_evaluate(clf, features, labels, num_iters=1000, test_size=0.3):
    arr_accuracy = []
    arr_precision = []
    arr_recall = []
    first = True
	
    for trial in range(num_iters):
        features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=test_size)
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
		
        arr_accuracy.append(accuracy_score(labels_test, predictions))
        arr_precision.append(precision_score(labels_test, predictions))
        arr_recall.append(recall_score(labels_test, predictions))
		
        if trial % 10 == 0:
            if first:
                sys.stdout.write('\nProcessing')
            sys.stdout.write('.')
            sys.stdout.flush()
            first = False

	#print results		
    print (clf)
    print ("precision: {}".format(mean(arr_precision)))
    print ("recall:    {}".format(mean(arr_recall)))
    print ("accuracy:  {}".format(mean(arr_accuracy)))
	
    return mean(arr_precision), mean(arr_recall),mean(arr_accuracy)

#Naive bayes

GNB_clf_org = GaussianNB()
GNB_clf_new = GaussianNB()

#SVM

SVM_clf_org = SVC(kernel='poly', C=1,gamma=1,random_state=42)
SVM_clf_new = SVC(kernel='poly', C=1,gamma=1,random_state=42)

#Decision Tree

DT_clf_org = DecisionTreeClassifier(min_samples_split = 20,min_samples_leaf=20)
DT_clf_new = DecisionTreeClassifier(min_samples_split = 20,min_samples_leaf=20)

#AdaBoost

AdaB_clf_org = AdaBoostClassifier(algorithm='SAMME')
AdaB_clf_new = AdaBoostClassifier(algorithm='SAMME')

#Navie Bayes model without new features
print ("")
print("Evaluate navie bayes model without new feature")
model_evaluate(GNB_clf_org, features, labels)

#Navie Bayes model with new feature
print ("")
print("Evaluate navie bayes model with new feature")
model_evaluate(GNB_clf_new, new_features, new_labels)

#SVM model without new feature
print ("")
print("Evaluate svm model without new feature")
model_evaluate(SVM_clf_org, features, labels)

#VM model with new feature
print ("")
print("Evaluate svm model with new feature")
model_evaluate(SVM_clf_new, new_features, new_labels)

#Decision Tree model without new feature
print ("")
print("Evaluate Decision Tree model without new feature")
model_evaluate(DT_clf_org, features, labels)

#Decision Tree model with new feature
print ("")
print("Evaluate Decision Tree model with new feature")
model_evaluate(DT_clf_new, new_features, new_labels)

#Adaboost model without new feature
print ("")
print("Evaluate Adaboost model without new feature")
model_evaluate(AdaB_clf_org, features, labels)

#Adaboost model with new feature
print ("")
print("Evaluate Adaboost model with new feature")
model_evaluate(AdaB_clf_new, new_features, new_labels)
print ("")

# Example starting point. Try investigating other evaluation techniques!
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

print ("")
test_classifier(GNB_clf_org, my_dataset, without_new_features_list)
print ("")
dump_classifier_and_data(GNB_clf_org, my_dataset, without_new_features_list)
