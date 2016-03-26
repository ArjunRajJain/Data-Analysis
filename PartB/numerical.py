#Data Stuff
from pandas import Series,DataFrame,read_csv
from numpy import amax
import copy
import re


#ML Stuff
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import cross_val_score

#subset of fields based upon their attributes

#these ones you can drop as there is no data
drop = ["interest_rate","wtd_loans","interest_rate","num_rate","numrate"]

#these have strings
categorical = ["term","int_rate","int_rate2","emp_length","earliest_cr_line","home_ownership","loan_status","purpose","addr_state","earliest_cr_line"];

#these are numbers
numerical = ["loan_amnt","funded_amnt","annual_inc","installment","dti","delinq_2yrs","mths_since_last_delinq","open_acc","revol_bal","total_acc","out_prncp","total_pymnt","total_rec_prncp","total_rec_int"];

#these are numbers with strings
extract_num = ["term","int_rate","int_rate2"]

#all features
features = ["emp_length","home_ownership","loan_status","purpose","addr_state","loan_amnt","funded_amnt","annual_inc","int_rate","installment","dti","delinq_2yrs","earliest_cr_line","mths_since_last_delinq","open_acc","revol_bal","total_acc","out_prncp","total_pymnt","total_rec_prncp","total_rec_int","int_rate2","term","int_rate"]

def clean_data(data):

    #drop unnecessary data
    data = data.drop(categorical + drop,axis = 1)

    #get max of all columns to do scaling
    max_data = amax(data, 0)

    for feature in numerical :
        #fill in nulls
        data[feature] = data[feature].fillna(0)

        #scale to 0-1
        if(not type(max_data[feature]) is str) :
            data[feature] = data[feature]/max_data[feature]

    return data;

def create_submission(name,alg, train, test, fields, filename):
    #lets fit and predict!
    alg.fit(train[fields], train["good"])

    predictions = alg.predict(test[fields]);

    #lets see our average score with cross_validation
    scores = cross_val_score(alg,test[fields],test["good"],cv=5);
    print("Accuracy for %s: %0.2f (+/- %0.2f)" % (name,scores.mean(), scores.std() * 2))

    #lets export our results to a csv
    submission = DataFrame({
        "id": test["id"],
        "good": predictions
    })
    submission.to_csv(filename, index=False);


    #lets get our co-effecients for each feature from the algorithm
    #and export it to a csv
    coeff_df = DataFrame(train[fields].columns)
    coeff_df.columns = ['Features']

    if type(alg) == LogisticRegression :
        coeff_df["Coefficient Estimate"] = alg.coef_[0];

    elif type(alg) == GaussianNB :
        coeff_df["Mean for Good"] = alg.theta_[0];
        coeff_df["Variance for Good"] = alg.sigma_[0];
        coeff_df["Mean for Bad"] = alg.theta_[1];
        coeff_df["Variance for Bad"] = alg.sigma_[1];
        coeff_df["Prior Probability for Good"] = [alg.class_prior_[1] for i in range(len(alg.theta_[0])) ]
        coeff_df["Prior Probability for Bad"] = [alg.class_prior_[0] for i in range(len(alg.theta_[0])) ]

    elif type(alg) == RandomForestClassifier:
        coeff_df["Feature Importance"] = alg.feature_importances_

    coeff_df.to_csv("coeff-"+ filename,index=False);



def main() :
    train_data = clean_data(read_csv("input/test.csv"))
    test_data  = clean_data(read_csv("input/train.csv"))

    predictors = [numerical]

    algos = [
        ("Gausian Naive Bayes","gausian_naive_bayes",GaussianNB()),
        ("K Neighbors Classifier","k_neighbors",KNeighborsClassifier(n_neighbors = 4)),
        ("Logistic Regression","logistic",LogisticRegression(random_state=1)),
        ("Random Forest Classifier","random_forest",RandomForestClassifier(
            random_state=1,
            n_estimators=100,
            min_samples_split=4,
            min_samples_leaf=2
        ))
    ];
    for fields in predictors :
        for alg in algos :
            create_submission(alg[0], alg[2], train_data, test_data,fields, alg[1]+".csv")



if __name__ == '__main__':
    main()
