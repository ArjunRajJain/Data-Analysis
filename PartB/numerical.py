#Data Stuff
from pandas import Series,DataFrame,read_csv
import copy
import re

#ML Stuff
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
from sklearn import metrics

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
    data.drop(categorical + drop,axis = 1)

    for feature in features :
        data[feature] = data[feature].fillna(0)

    return data;

def create_submission(name,alg, train, test, fields, filename):
    #lets fit and predict!
    alg.fit(train[fields], train["good"])

    predictions = cross_validation.cross_val_predict(
        alg,
        test[fields],
        test["good"],
        cv=2
    );

    #lets see our average score with cross_validation
    print "Mean Score for ", name , " - ", metrics.accuracy_score(test["good"], predictions);


    #lets export our results to a csv
    submission = DataFrame({
        "id": test["id"],
        "good": predictions
    })
    submission.to_csv(filename, index=False);


    #lets get our co-effecients for each feature from the algorithm
    #and export it to a csv
    coeff_df = DataFrame(train.columns.delete(0))
    coeff_df.columns = ['Features']

    if type(alg) == LogisticRegression :
        coeff_df["Coefficient Estimate"] = Series(alg.coef_[0])
    elif type(alg) == GaussianNB :
        coeff_df["Coefficient Estimate"] = Series(alg.theta_[0])
    elif type(alg) == KNeighborsClassifier :
        coeff_df["Coefficient Estimate"] = Series(alg.getParams())
    elif type(alg) == RandomForestClassifier:
        coeff_df["Feature Importance"] = Series(alg.feature_importances_)

    coeff_df.to_csv("coeff-"+ filename,index=False);



def main() :
    train_data = clean_data(read_csv("input/test.csv"))
    test_data  = clean_data(read_csv("input/train.csv"))

    predictors = [numerical]

    algos = [
        ("Gausian Naive Bayes","gausian_naive_bayes",GaussianNB()),
        ("K Neighbors Classifier","k_neighbors",KNeighborsClassifier(n_neighbors = 3)),
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
