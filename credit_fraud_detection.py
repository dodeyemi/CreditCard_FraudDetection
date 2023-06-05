# -*- coding: utf-8 -*-
"""Credit Fraud Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AbByv33HouGI8szHNXLhMDVG1oXMeb2z

##**Credit Card Fraud Detection**##

Machine learning has emerged as a powerful tool in detecting credit card fraud in the UK. Leveraging vast amounts of data and advanced algorithms, machine learning models can analyze patterns, anomalies, and historical fraud cases to identify fraudulent transactions accurately.

These models are trained on extensive datasets that include both legitimate and fraudulent transactions, enabling them to learn the characteristics and patterns associated with fraudulent activities. By analyzing factors such as transaction amount, location, time, and user behavior, machine learning algorithms can detect deviations from normal patterns and flag potentially fraudulent transactions in real-time.

Machine learning-based fraud detection systems in the UK continuously evolve as they learn from new fraud patterns and adapt to emerging threats. These systems can reduce false positives and negatives, leading to more accurate fraud identification and minimizing disruption to legitimate cardholders.

Collaboration between financial institutions, payment processors, and data scientists is crucial in developing effective machine learning models. Sharing anonymized transaction data and collaborating on research helps improve the performance and effectiveness of fraud detection algorithms.

Machine learning-based detection systems serve as an essential defense against credit card fraud in the UK, enhancing security measures and safeguarding the financial well-being of both consumers and financial institutions.

In this research, we will use machine learning apprach to detect credit card frauds and also contribute to existing research on this topic.

##**Data Reading**##

This data is available in the google drive and google drive will be the primary location of storing the credit card fraud data. We will as well read the data from the same location.
"""

from google.colab import drive # The code reading the folder containing all the images in the zip folders on google drive

drive.mount("/content/gdrive")

"""##**Libraries**##

Machine learning and Analytics basically relies on different libraries. These libraries are listed and imported below:
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split #
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score,roc_auc_score

"""**Data Reading**

The data is read from csv files available in google drive and is assigned to a variable called "Data" below:
"""

Data = pd.read_csv('/content/gdrive/MyDrive/creditcard.csv')
Data.head(3)

"""Describe the data to show the summary of the entire datasest."""

Data.describe()

"""**Data Types**
The data types are shown with the function below: There are different kinds of data types. They are float, int, object etc.
"""

Data.dtypes

"""**Target Analysis**

Targets are like the end result of every experiment. It is a guiding variable to any experiment. It is the only variable to predict. In this research, the target variable is the class. And the class only have two levels. This makes this a binary classification problem. 0 here is the non-fradulent customers and the 1 represent the fraudulent customers.
"""

Data['Class'].unique()

Groupby_Data = Data.groupby('Class')['Amount'].count().reset_index()
sns.barplot(x= 'Class', y= 'Amount', data= Groupby_Data)

"""**Aggregate Function**

This aspect enables us to show the count of the entire datasets, the fraudulent cases and non-fraudulent cases.
"""

Data['Class'].count() #Total count

Fraud_Cases = Data[Data['Class'] == 1]
Fraud_Cases['Class'].count() # Fraudulent Cases

Non_Fraudulent = Data[Data['Class'] == 0]
Non_Fraudulent['Class'].count() #Non fraudulent cases.

sns.histplot(x ='Amount', data= Data )
plt.title('Distribution of CreditCard DisbursedAmounts')
plt.xlabel('Disbursement Values')
plt.ylabel('Volumes') # Histograms of the amount disbursed.

Features = Data.drop('Class', axis = 1) # Ascribing the Features variable in a seperate variables and removing the target which is the Class.
#Features.dtypes

Class = Data['Class']
Class.tail(5)

"""##**Feature Selection**##

There are different methods of feature selection. In this research, we will be using only a few that are listed below.

1. The Heatmap method
2. Chi2
3. Xtra Tree Clssifier.
4. F.Regression.

**Heatmap Technic**
"""

Correlation = Data.corr().round(2)
sns.set(rc={'figure.figsize':(40,20)})
sns.heatmap(Correlation,xticklabels = Correlation.columns, yticklabels=Correlation.columns, annot = True)

"""##Chi2##"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression, chi2


# Apply the MinMaxScaler to scale the features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(Features)

# Apply the KBest feature selection
k = 10  # Number of best features to select
kbest = SelectKBest(score_func=chi2, k=k)
selected_features = kbest.fit_transform(X_scaled, Class)

# Get the indices of the selected features
selected_indices = kbest.get_support(indices=True)

# Get the names of the selected features
selected_feature_names = Features.columns[selected_indices]

# Print the selected feature names
print("Selected Features:")
for feature in selected_feature_names:
    print(feature)

"""##**F-Regressions**##"""

from sklearn.feature_selection import SelectKBest, f_regression, chi2


# Apply the KBest feature selection
k = 10  # Number of best features to select
kbest = SelectKBest(score_func=f_regression, k=k)
selected_features = kbest.fit_transform(Features, Class)

# Get the indices of the selected features
selected_indices = kbest.get_support(indices=True)

# Get the names of the selected features
selected_feature_names = Features.columns[selected_indices]

# Print the selected feature names
print("Selected Features:")
for feature in selected_feature_names:
    print(feature)

"""##**Extra Tree Classifier**##"""

import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier

# Feature selection with ExtraTreeClassifier
model = ExtraTreesClassifier()
model.fit(Features, Class)

# Get feature importances
importances = model.feature_importances_

# Sort feature importances in descending order
indices = np.argsort(importances)[::-1]

# Select the top 10 features
k = 10  # Number of best features to select
selected_indices = indices[:k]
selected_features = Features.columns[selected_indices]
selected_importances = importances[selected_indices]

# Plot bar chart
plt.figure(figsize=(10, 6))
plt.bar(selected_features, selected_importances)
plt.xticks(rotation=65)
plt.xlabel("Features")
plt.ylabel("Feature Importance")
plt.title("Top 20 Features - ExtraTreeClassifier Model")
plt.tight_layout()
plt.show()

"""##**Oversampling**##

This classification problem is sure not a balance one. The imbalance ratio is very wide. There is need to oversample the minority class to have a 1:1 ratio. This process is as seen below:

"""

import matplotlib.pyplot as plt
from imblearn.over_sampling import RandomOverSampler

# Original dataset counts
minority_class_count = Fraud_Cases['Class'].count() 
majority_class_count = Non_Fraudulent['Class'].count()

# Create an oversampler instance
oversampler = RandomOverSampler(sampling_strategy='minority')

# Reshape the target variable to match the expected format
Class = np.array(Class).reshape(-1, 1)

# Perform oversampling
X_resampled, y_resampled = oversampler.fit_resample(Features, Class)

# Check the new class distribution
unique, counts = np.unique(y_resampled, return_counts=True)
class_distribution = dict(zip(unique, counts))

# Print class distribution after oversampling
print("Class distribution after oversampling:", class_distribution)

# Plot the bar chart
plt.bar(class_distribution.keys(), class_distribution.values())
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution after Oversampling')
plt.show()

#X_resampled.dtypes
y_resampled

"""##Split the Data into Training and Testing##

To prepare the the data for machine learning, there is need to bisect the data into training and testing data with a ratio of 80: 20. This is seen below:
"""

#Spliting the PPS_BioData datasets into training and testing.
X_train, X_test, y_train, y_test = train_test_split(Features, Class, stratify= Class,test_size=0.2)
print('Shapes XTrain:', X_train.shape) #Print the shape of the x-train
print('Shapes XTest:', X_test.shape)

"""##Fit and Evaluate Regression Model##

We will be fitting and evluating the model on all the features at this stage.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
model = LogisticRegression()

# fit model
model.fit(X_train, y_train)

# predict on test set
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# evaluation metrics
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Precision:', precision_score(y_test, y_pred))
print('Recall:', recall_score(y_test, y_pred))
print('F1 score:', f1_score(y_test, y_pred))
print('ROC AUC score:', roc_auc_score(y_test, y_prob))
#Confusion Matrix of the Model.
print('Confusion matrix:\n', confusion_matrix(y_test, y_pred))

"""**Comments**

The logistics regression model metrics above shows the model fairly perform well in terms of predicting positive and negative cases. There are 79 wrong predictions as seen in the confusion matrix.

**VISUALISATION: AUC AND CONFUSION MATRIX**

These two metrics shows the overall model performance. It is visualised below: The AUC in particular shows how the model is able to predict both positive and negative cases correctly.
"""

from sklearn.metrics import roc_curve, auc
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic(ROC) Curve')
plt.legend(loc="lower right")
plt.show()

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Generate confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix
plt.imshow(conf_mat, cmap='Greens', interpolation='None')
plt.colorbar()

plt.xticks([0, 1], ['Class 0', 'Class 1'])
plt.yticks([0, 1], ['Class 0', 'Class 1'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')

for i in range(conf_mat.shape[0]):
    for j in range(conf_mat.shape[1]):
        plt.annotate(str(conf_mat[i][j]), xy=(j, i), ha='center', va='center')

plt.show()

"""##Fitting and Evaluating a CNN Model##

Here we will still use the all features to build and evaluate a CNN model.
"""

import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
import numpy as np

np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)

# Assuming X_train and X_test are numpy arrays
# Reshape data for CNN model
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))

# Reshape data to 3D format for CNN model
X_train = np.expand_dims(X_train, axis=2)
X_test = np.expand_dims(X_test, axis=2)

# Create CNN model
modelcnn = Sequential()
modelcnn.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
modelcnn.add(MaxPooling1D(pool_size=2))
modelcnn.add(Flatten())
modelcnn.add(Dense(64, activation='relu'))
modelcnn.add(Dropout(0.5))
modelcnn.add(Dense(1, activation='sigmoid'))

# Compile the model
modelcnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
modelcnn.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Compile model
# Compile model
np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)

modelcnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit model
history = modelcnn.fit(X_train, y_train, batch_size=64, epochs=10, verbose=1, validation_data=(X_test, y_test))

# Evaluate model on test data
y_pred2 = modelcnn.predict(X_test)
y_pred_classes = (y_pred2 > 0.5).astype('int32')

accuracy = accuracy_score(y_test, y_pred_classes)
precision = precision_score(y_test, y_pred_classes)
recall = recall_score(y_test, y_pred_classes)
auc = roc_auc_score(y_test, y_pred2)


print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('AUC:', auc)

"""**Comments**
The CNN model metrics is not a good one for this type of datasets as it has avery high error rate compared to others. The recall and precision are zero which is a redflag.
"""

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Convert y_pred2 to binary values (0 or 1)
y_pred2_binary = np.round(y_pred2)

# Generate confusion matrix
conf_mat2 = confusion_matrix(y_test, y_pred2_binary)

# Plot the confusion matrix
plt.imshow(conf_mat2, cmap='Greens', interpolation='None')
plt.colorbar()

plt.xticks([0, 1], ['Class 0', 'Class 1'])
plt.yticks([0, 1], ['Class 0', 'Class 1'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')

for i in range(conf_mat2.shape[0]):
    for j in range(conf_mat2.shape[1]):
        plt.annotate(str(conf_mat2[i][j]), xy=(j, i), ha='center', va='center')

plt.show()

"""##Using The Best 10 Features to fit a SVM Model##

Below are ten best features relevant to the class and these will be used for fitting and evaulauting the machine learning models.
"""

Features_New = Features.drop(['V1','V2','V5','V6','V8','V9','V13','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28'], axis = 1)
Features_New.dtypes

#Spliting the PPS_BioData datasets into training and testing.
X_train1, X_test1, y_train1, y_test1 = train_test_split(Features_New, Class, stratify= Class,test_size=0.2)
print('Shapes XTrain:', X_train1.shape) #Print the shape of the x-train
print('Shapes XTest:', X_test1.shape)

"""##Logistics Regression##"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
model3 = LogisticRegression()

# fit model
model3.fit(X_train1, y_train1)

# predict on test set
y_pred3 = model3.predict(X_test1)
y_prob3 = model3.predict_proba(X_test1)[:, 1]

# evaluation metrics
print('Accuracy:', accuracy_score(y_test1, y_pred3))
print('Precision:', precision_score(y_test, y_pred3))
print('Recall:', recall_score(y_test, y_pred3))
print('F1 score:', f1_score(y_test, y_pred3))
print('ROC AUC score:', roc_auc_score(y_test, y_prob3))
#Confusion Matrix of the Model.
print('Confusion matrix:\n', confusion_matrix(y_test, y_pred3))

"""**Comments**

This model is not better in any way. There are lots of misclassifications. The confusion matrix shows 188 wrong predictions and the positive predictions were all wrong. However, using the best 10 features did not improve the performance of the model still

##SVM Model##
"""

from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)
# Create an SVM model
svm_model = SVC()

# Fit the model on the training data
svm_model.fit(X_train1, y_train1)

# Predict the classes for the test set
y_pred4 = svm_model.predict(X_test1)

# Generate the classification report
report = classification_report(y_test1, y_pred4)
print("Classification Report:")
print(report)

# Generate the confusion matrix
confusion_mat4 = confusion_matrix(y_test1, y_pred4)
print("Confusion Matrix:")
print(confusion_mat4)

# Calculate recall and precision
true_positive = confusion_mat4[1, 1]
false_negative = confusion_mat4[1, 0]
false_positive = confusion_mat4[0, 1]

recall = true_positive / (true_positive + false_negative)
precision = true_positive / (true_positive + false_positive)

print("Recall:", recall)
print("Precision:", precision)

# Calculate AUC
auc = roc_auc_score(y_test, y_pred)
print("AUC:", auc)

"""##Fit Model Without Balancing the Classes##

Ordinarily, this stage should have actually come first. It is about fitting the model without addressing the imbalanced classes. 

In this session , we shall go through the models again and run some other ones.
"""

Class1 = Data['Class']
Class1.dtypes

Features1 = Data.drop('Class', axis = 1)
Features1.dtypes

X_train2, X_test2, y_train2, y_test2 = train_test_split(Features1, Class1, stratify= Class1,test_size=0.2)
print('Shapes XTrain:', X_train2.shape) #Print the shape of the x-train
print('Shapes XTest:', X_test2.shape)

from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)
# Create an SVM model
svm_model2 = SVC()

# Fit the model on the training data
svm_model2.fit(X_train2, y_train2)

# Predict the classes for the test set
y_pred5 = svm_model2.predict(X_test2)

# Generate the classification report
report5 = classification_report(y_test2, y_pred5)
print("Classification Report:")
print(report)

# Generate the confusion matrix
confusion_mat5 = confusion_matrix(y_test2, y_pred5)
print("Confusion Matrix:")
print(confusion_mat5)

# Calculate recall and precision
true_positive = confusion_mat5[1, 1]
false_negative = confusion_mat5[1, 0]
false_positive = confusion_mat5[0, 1]

recall = true_positive / (true_positive + false_negative)
precision = true_positive / (true_positive + false_positive)

print("Recall:", recall)
print("Precision:", precision)

# Calculate AUC
auc = roc_auc_score(y_test, y_pred)
print("AUC:", auc)

"""##Logistics Regression on Imbalanced Data##"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
model5 = LogisticRegression()

# fit model
model5.fit(X_train2, y_train2)

# predict on test set
y_pred6 = model5.predict(X_test2)
y_prob6 = model5.predict_proba(X_test2)[:, 1]

# evaluation metrics
print('Accuracy:', accuracy_score(y_test2, y_pred6))
print('Precision:', precision_score(y_test, y_pred6))
print('Recall:', recall_score(y_test, y_pred6))
print('F1 score:', f1_score(y_test, y_pred6))
print('ROC AUC score:', roc_auc_score(y_test2, y_prob6))
#Confusion Matrix of the Model.
print('Confusion matrix:\n', confusion_matrix(y_test2, y_pred6))

"""##Random Forest Model##"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)

# Create a Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train2, y_train2)

# Predict on the test set
y_pred7 = rf_classifier.predict(X_test2)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test2, y_pred7)
precision = precision_score(y_test2, y_pred7)
recall = recall_score(y_test2, y_pred7)
f1 = f1_score(y_test2, y_pred7)

# Print the evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

"""##Confusion Matric for Random Forest##"""

# Convert y_pred2 to binary values (0 or 1)
y_pred2_binary = np.round(y_pred7)

# Generate confusion matrix
confusion_mat5 = confusion_matrix(y_test2, y_pred2_binary)

# Plot the confusion matrix
plt.imshow(confusion_mat5, cmap='Greens', interpolation='None')
plt.colorbar()

plt.xticks([0, 1], ['Class 0', 'Class 1'])
plt.yticks([0, 1], ['Class 0', 'Class 1'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')

for i in range(confusion_mat5.shape[0]):
    for j in range(confusion_mat5.shape[1]):
        plt.annotate(str(confusion_mat5[i][j]), xy=(j, i), ha='center', va='center')

plt.show()

"""##AUC For Random Forest##"""

from sklearn.metrics import roc_curve, auc
fpr, tpr, thresholds = roc_curve(y_test2, y_pred7)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic(ROC) Curve')
plt.legend(loc="lower right")
plt.show()

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

np.random.seed(42)

# Set the seed for TensorFlow
tf.random.set_seed(42)

# Create a Naive Bayes classifier
nb_classifier = GaussianNB()

# Train the classifier
nb_classifier.fit(X_train2, y_train2)

# Predict on the test set
y_pred8 = nb_classifier.predict(X_test2)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test2, y_pred8)
precision = precision_score(y_test2, y_pred8)
recall = recall_score(y_test2, y_pred8)
f1 = f1_score(y_test2, y_pred8)

# Print the evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

"""##Testing with Validation Data##

Here, after getting the right model that is able to predict the fraudulent and nonfraudulent credit card transactions, we will be validating the model with another datasets that are randomly selected from the original datasets to re-validate the quality of the model decisions.
"""

import random
Data_Val= Data.sample(n=1000, random_state=random.seed(222))
Data_Val

Class3 = Data_Val['Class']
Class3

Feature3 = Data_Val.drop('Class', axis = 1)
Feature3

# Predict on the test set
y_pred9 = rf_classifier.predict(Feature3)

# Calculate evaluation metrics
accuracy = accuracy_score(Class3, y_pred9)
precision = precision_score(Class3, y_pred9)
recall = recall_score(Class3, y_pred9)
f1 = f1_score(Class3, y_pred9)

# Print the evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

"""**Comments**

From the model metrics on the 1000 validation datasets, it is evidenced that the model still perfroms very well and it is able to predict all negative and positive cases correctly.
"""

# Convert y_pred2 to binary values (0 or 1)
y_pred2_binary1 = np.round(y_pred9)

# Generate confusion matrix
confusion_mat9 = confusion_matrix(Class3, y_pred2_binary1)

# Plot the confusion matrix
plt.imshow(confusion_mat9, cmap='Greens', interpolation='None')
plt.colorbar()

plt.xticks([0, 1], ['Class 0', 'Class 1'])
plt.yticks([0, 1], ['Class 0', 'Class 1'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')

for i in range(confusion_mat9.shape[0]):
    for j in range(confusion_mat9.shape[1]):
        plt.annotate(str(confusion_mat9[i][j]), xy=(j, i), ha='center', va='center')

plt.show()

Count_FraudVal = Class3[Class3==1]
Count_FraudVal.count()