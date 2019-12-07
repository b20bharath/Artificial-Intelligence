# import the required libraries for operations and reading the input
import pandas as pd
import numpy as np
ep = np.finfo(float).eps
from numpy import log2 as log
from scipy.stats import chi2, chi2_contingency
from pprint import pprint
#reading the data from csv file
url = 'https://raw.githubusercontent.com/aimacode/aima-data/master/restaurant.csv'
alpha = 0.05                    #significance level = 0.05
data = pd.read_csv(url,header=None)
#stripping the values in the dataset
for col in data.columns:
    value = data[col].tolist()
    for i in range(len(value)):
        value[i] = value[i].strip()
    data[col] = value
#changing the values to numeric
data_Attributes = ['Alt','Bar','Fri','Hun','Pat','Price','Rain','Res','Type','Est','WillWait']
changevalues = {'Yes':1,'No':0}
changevalues1 = {'None':0,'Some':1,'Full':2}
changevalues2 = {'$':0,'$$':1,'$$$':2}
changevalues3 = {'Burger':0,'Thai':1,'Italian':2,'French':3}
changevalues4 = {'0-10':0,'10-30':1,'30-60':2,'>60':3}
for col in [0,1,2,3,6,7,10]:
    data[col] = data[col].map(changevalues)

data[4]= data[4].map(changevalues1)
data[5] = data[5].map(changevalues2)
data[8] = data[8].map(changevalues3)
data[9] = data[9].map(changevalues4)
Iteration = {'Iteration':1,'Attributes':[],'Information Gain':[],'Attribute to split':''}
informationGain = []
Attributes = []

def attrEntropy(data,attr):                     #calculating the entropy for each attribute
    classification = data.columns[-1]
    var = data[attr].unique()
    classes = data[classification].unique()
    entropy = 0
    for v in var:
        e = 0
        for cl in classes:
            proportion = (len(data[attr][data[attr]==v][data[classification]==cl]))/((len(data[attr][data[attr]==v]))+ep)
            e = e+ (-(proportion*np.log2(proportion+ep)))
        f = (len(data[attr][data[attr]==v]))/len(data)
        entropy = entropy + (-f*e)
    return abs(entropy)

def split(data):                                #getting the best attribute for splitting based on information gain
    ent_attr = []
    information_gain = []
    classification = data.columns[-1]
    root_ent = 0
    classes = data[classification].unique()
    for cl in classes:
        proportion = (data[classification].value_counts()[cl])/len(data[classification])
        root_ent = root_ent + (-(proportion*np.log2(proportion)))
    column = data.columns[:-1]
    for col in column:
        information_gain.append(round((root_ent - attrEntropy(data,col)),2))
    informationGain = information_gain[:]
    Iteration['Information Gain'] = informationGain
    Iteration['Attributes'] = column[:]
    return column[np.argmax(information_gain)]


modify = {'Alt': {0:'No',1:'Yes'},'Bar': {0:'No',1:'Yes'},'Fri': {0:'No',1:'Yes'},'Hun': {0:'No',1:'Yes'},'Pat': {0:'None', 1:'Some', 2:'Full'},'Price': {0:'$',1:'$$',2:'$$$'},'Rain': {0:'No',1:'Yes'},'Res': {0:'No',1:'Yes'},'Type': {0:'Burger',1:'Thai',2:'Italian',3:'French'},'Est': {0:'0-10',1:'10-30',2:'30-60',3:'>60'}}
def DecisionTree(data,decisiontree=None):                           #Decision Tree function
    classification = data.columns[-1]
    split_attr = split(data)
    Iteration['Attribute to split'] = data_Attributes[split_attr]
    print('SPLIT:',Iteration['Iteration'])
    attrib = []
    for col in Iteration['Attributes']:
        attrib.append(data_Attributes[col])
    print('Attributes:',attrib)
    print('Information Gain:',Iteration['Information Gain'])
    print('Attribute to split on:',Iteration['Attribute to split'])
    print('\n')
    Iteration['Iteration'] = Iteration['Iteration'] + 1
    values = data[split_attr].unique()
    sp = data_Attributes[split_attr]
    if decisiontree is None:                                        #forming the decision tree dictionary with best attribute for splitting
        decisiontree = {}
        decisiontree[data_Attributes[split_attr]] = {}
    for val in values:
        split_data = data[data[split_attr] == val].reset_index(drop=True)
        class_value,count = np.unique(split_data.iloc[:,-1],return_counts=True)
        split_data=split_data.drop([split_attr],axis = 1)
        mod = modify[sp]
        val = mod[val]
        if len(count) == 1:
            if(class_value[0] == 0):
                decisiontree[data_Attributes[split_attr]][val] = 'No'
            else:
                decisiontree[data_Attributes[split_attr]][val] = 'Yes'
        else:
            decisiontree[data_Attributes[split_attr]][val] = DecisionTree(split_data)
    return decisiontree


decisionTree = DecisionTree(data)

print('The Decision Tree obtained with mapped values is:\n')
pprint(decisionTree)

#chi-square pruning technique on the resulting decision tree
spliters = []
y_class = data.iloc[:,-1]
predictors = data.iloc[:,:-1]
count = 0
for col in predictors.columns:
    cont = pd.crosstab(predictors[col], y_class)
    test_statistic, p, degree_freedom, expected = chi2_contingency(cont)
    if test_statistic > chi2.isf(q=alpha, df=degree_freedom):
        spliters.append(data_Attributes[count])
    count = count+1

def prune(decisiontree):                            #prune the decision tree
    global flag
    leaf = True
    root = None
    for item in decisiontree:
        if isinstance(decisiontree[item], dict):
            leaf = False
            root = item
            break
    
    if leaf and ([x for x in decisiontree.keys()][0].split(' ')[0]) not in spliters:
        flag = True
        return 0
    if(leaf == False):
        if prune(decisiontree[root]):
            decisiontree[root] = None
    return decisiontree
        

flag = False

x = list(decisionTree.keys())[0]
if x in spliters:
    decisionTree = prune(decisionTree[x])
else:
    decisionTree = None

print('--------------------------------------------------------------------')
print('Decision Tree after pruning:')
DT = {x:decisionTree}
pprint(DT)