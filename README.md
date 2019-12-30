# Predict-Medical-Appointment-No-Shows

## 1. Introduction

Patient no-show has long been an issue in healthcare field. As limited medical resources are available, a no-show occurrence means not only inadequate care for the patient which might lead to poorer patient health, but also a waste of scarce healthcare resources. Accurate prediction of patient no-show could help to optimize allocation of valuable doctor time by scheduling more patients for the visit time if a no-show is likely to happen, as well as to effectively reduce appointment no-shows by providing intervention like reminder calls to targeted high-risk population. Therefore, to predict patient no-show accurately is a task of vital significance yet waiting to be done. 

Previous studies, of which there are not many, achieved accuracy around 0.7 in their models. We believe we could do better than that. And moreover, besides focusing on accuracy improvement, we also target on precision and recall, which are even more important than accuracy when considering real world application.

## 2. Empirical Analysis

### 2.1 Data
We obtained the data from [Kaggle](https://www.kaggle.com/joniarroba/noshowappointments). The data set contains 2 months of registration data, including 110,527 scheduled appointments and 14 variables. The dependent variable in this analysis is the binary variable No-show, indicating whether the patient attended their scheduled appointments. Other variables include patients’ identifier (patient ID and appointment ID), demographics (age, gender), medical conditions (alcoholism, hypertension, diabetes), geographic location (neighborhood), receiving reminder messages, schedule date, and appointment date, etc. Table 1 shows the distribution of patient characteristics by no-show outcome.
![Table1](https://github.com/stemgene/Predict-Medical-Appointment-No-Shows/blob/master/Images/table1.png)

### 2.2 Data Preprocessing
We performed the following data preprocessing strategies and addressed the class imbalanced issue:

A) Age: we removed patients under 0-year-old and normalized the variable.

B) Lead time: previous literature indicates that lead time (time interval between schedule day and the actual appointment day) is one of the strong predictors of no-show, we thus constructed this variable using the variables ScheduleDay and AppointmentDay in our dataset. Another important predictor is the day of week, which may affect patient’s behavior. Therefore, we created a new feature “day of week” using the variable AppointmentDay.                                         

C)  Index variables: “PatientID”, “AppointmentID”
From the data we found that one PatientID could have multiple different AppointmentIDs, indicating that the patients may schedule appointments multiple times within the study time period. We checked on the distribution of number of visits per patient and excluded patients who made so many appointments.
We draw a pie plot to show the proportion of number of visits per patient (Figure 1). Among the overall 62299 patients, we found that about 40% of patients showed up more than once, and 1421 (2.3%) patients made appointments more than 5 times. We considered patients who made appointments more than 8 times as outliers (the top 1%) and removed them from our dataset. 
![Figure1](https://github.com/stemgene/Predict-Medical-Appointment-No-Shows/blob/master/Images/3221FBE9-B970-42D6-8B83-685D66EAD579.png)

D) Location information: “Neighborhood”
Patients’ geographical information was specified to the town level in our dataset. There are 81 towns in Victoria, a city in Brazil. We counted the number of patients within each town and the distribution is shown in Figure 2.
![Fiture2](https://github.com/stemgene/Predict-Medical-Appointment-No-Shows/blob/master/Images/figure2.png)

Considering that some of these 81 towns only have a small number of patients, we used the unsupervised K_means to group towns into larger clusters. Finally, we grouped the 81 towns into 15 clusters, and almost all of them contain more than 5000 patients.

![Fiture3](https://github.com/stemgene/Predict-Medical-Appointment-No-Shows/blob/master/Images/Figure3.png)

E) No-show history
From some literature, a patient’s no-show history would be a very important feature. Hence we calculated the no-show rate before current patient visit based on “Patient ID” and “No-show” label together. Noteworthily, we created a new feature to distinguish new patients with other patients who truly had zero no-show rate for previous visits (clean sheet).

F) Class imbalance
As shown in Table 1, there were 22,319 (20.19%) missed appointments in our dataset, indicating the issue of class imbalance. We doubled the observations in the minority class and randomly sampled an equal number of observations in the majority class to address this issue.

### 2.3 Models
We randomly split the data into the training set (75%), validation set (15%), and testing set (15%) based on the patient ID. We used the balanced training set to train the models, the balanced validation set was used for hyperparameter tuning, and model performance was evaluated on the unbalanced testing set. Our predictive models include logistic regression, SVM, random forest, and neural network. Considering that patients under 18 years old may behave differently and have different medical conditions than older patients, we ran the analysis on the sample of patients over 18 years old. As another sensitivity analysis, we also ran the models with the original Neighborhood variable.

## 3. Results

Model performance was evaluated by precision, recall, and accuracy. Table 2 summarizes the model performance on the validation and testing set. As can be seen from this table, logistic regression and SVM did not perform well on our sample, even after hyperparameter tuning. Random forest model produced the best results, with a precision of 0.83, a recall of 0.73, and an accuracy of 0.91 on the testing set. Although the neural network resulted in a good performance on the validation set after fine-tuning, the precision and recall decreased to 0.47 at testing time. Results of the sensitivity analysis were included in the Appendix, where we did not observe significant differences from our main analysis.

<table>
  <tr>
    <th>  </th>
    <th colspan='2'><center>Linear Regression</center></th>
    <th colspan='2'><center>SVM</center></th>
    <th colspan='2'><center>Random Forest</center></th>
    <th colspan='2'><center>Neural Network</center></th>
  </tr>
  <tr>
    <td> Dataset </td>
    <td>Validation Set</td>
    <td>Testing Set</td>
    <td>Validation Set</td>
    <td>Testing Set</td>
    <td>Validation Set</td>
    <td>Testing Set</td>
    <td>Validation Set</td>
    <td>Testing Set</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td><center>0.32</center></td>
    <td><center>0.31</center></td>
    <td><center>0.29</center></td>
    <td><center>0.3</center></td>
    <td><center>0.82</center></td>
    <td><center>0.83</center></td>
    <td><center>0.84</center></td>
    <td><center>0.47</center></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td><center>0.59</center></td>
    <td><center>0.59</center></td>
    <td><center>0.88</center></td>
    <td><center>0.89</center></td>
    <td><center>0.72</center></td>
    <td><center>0.73</center></td>
    <td><center>0.78</center></td>
    <td><center>0.47</center></td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td><center>0.66</center></td>
    <td><center>0.66</center></td>
    <td><center>0.54</center></td>
    <td><center>0.54</center></td>
    <td><center>0.91</center></td>
    <td><center>0.91</center></td>
    <td><center>0.82</center></td>
    <td><center>0.78</center></td>
  </tr>
</table>

We performed variable importance analysis with logistic regression and random forest. The results are shown in the table 3 and Figure 4. These two models produced consistent variable importance, indicating that lead time, age, previous no-show rate, receiving reminder messages, and male gender are strong predictors of no-show outcome. Specifically, from Table 3 we can see that patients with long lead time, with diabetes and alcoholism, and having a high previous no-show rate were more likely to be no-show patients. Male patients and older patients were more likely to attend their appointments. Receiving reminder messages was positively associated with the outcome, one interpretation is that the reminder messages may only have been sent to patients who had nonattendance history.

<table>
  <tr>
    <th><center>Variables</center></th>
    <th><center>Coef.</center></th>
    <th><center>p_value</center></th>
  </tr>
  <tr>
    <td>Lead_Time</td>
    <td>0.0271</td>
    <td>0</td>
  </tr>
  <tr>
    <td>Diabetes</td>
    <td>0.1022</td>
    <td>0.0004</td>
  </tr>
  <tr>
    <td>Alcoholism</td>
    <td>0.2656</td>
    <td>0</td>
  </tr>
  <tr>
    <td>SMS_Received</td>
    <td>0.3538</td>
    <td>0</td>
  </tr>
  <tr>
    <td>Male</td>
    <td>-0.1676</td>
    <td>0</td>
  </tr>
  <tr>
    <td>Age_scaled</td>
    <td>-1.3964</td>
    <td>0</td>
  </tr>
  <tr>
    <td>Noshow_Rate</td>
    <td>-0.6419</td>
    <td>0</td>
  </tr>
</table>

<div align="center"><img width="500" src="https://github.com/stemgene/Predict-Medical-Appointment-No-Shows/blob/master/Images/Figure4.png"/></div>

## 4. Discussion

Random forest model had the best overall performance in our project. We ended up with a predicting model, a random forest model, with 0.83 precision, 0.73 recall, and 0.91 accuracy on our testing set, which exceeds almost all current published no-show prediction models. However, considering the real world application, though the accuracy is satisfying, the precision and recall are still not good enough. We tried all kinds of stuff to improve precision and recall, yet no big improvement was achieved. We identified two major limitations our models were suffering from that might account for the not-good-enough precision and recall. First, we only have 13 independent variables in our dataset. That means too few features were put into our models. Second, more than 50% patients only showed up once in our dataset thus we actually lacked more than half of the population's previous no-show information, which according to other studies is super important as a predictor. Due to the two major limitations in the dataset, we had difficulty in reaching better precision and recall. In the future studies, after including more features as well as having a longer time frame in the datasets, we believe a model with better precision and recall could be achieved which could assist designing interventions to address the appointment no-show issue to obtain an optimal allocation of scarce medical resources.

## Files
* noshowdata.csv
* forliummap.py: the code that generate the map, it needs two data files, 'noshowdata.csv' and 'towns.csv'.
* map3.html: the output of forliummap.py
