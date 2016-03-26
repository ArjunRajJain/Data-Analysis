#Data Stuff
from pandas import Series,DataFrame,read_csv, read_sql_table
from numpy import amax
import copy
import re
from sqlalchemy import create_engine


#ML Stuff
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split, cross_val_score

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

    #find out if the loan is good or not and add the appropriate column indicating so
    pattern = re.compile("(Current|Fully)")
    data["good"] = [1 if (type(status) is unicode or type(status) is str) and not pattern.search(status) == None else 0 for status in data["loan_status"]]

    #drop unnecessary data
    data = data.drop(categorical + drop,axis = 1)

    #fill in nulls
    for feature in numerical :
        data[feature] = data[feature].fillna(0)

    #scale data based on min-max
    data[numerical] = preprocessing.MinMaxScaler().fit_transform(data[numerical])

    return data;

def create_submission(name, alg, data, fields, filename):
    #lets fit and predict!
    x_train, x_test, y_train, y_test = train_test_split(
        data[fields+["id"]],
        data['good'],
        test_size=0.3,
        random_state=0
    )

    alg.fit(x_train[fields], y_train)
    predictions = alg.predict(x_test[fields]);

    #lets see our average score with cross_validation
    scores = cross_val_score(alg,x_test[fields],y_test,cv=10);
    print("Accuracy for %s: %0.2f (+/- %0.2f)\n" % (name,scores.mean(), scores.std() * 2))

    #lets export our results to a csv
    submission = DataFrame({
        "id": x_test["id"],
        "good": predictions
    })

    submission.to_csv("predictions/"+filename, index=False);

    #lets get our co-effecients for each feature from the algorithm
    #and export it to a csv
    coeff_df = DataFrame(x_test[fields].columns)
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

    coeff_df.to_csv("weights/"+ filename,index=False);


def main() :
    print "\nPulling Data\n"

    #set up db variables
    HOST = "sql-exercise.cnfbdodh0lq8.us-west-2.redshift.amazonaws.com";
    PORT,DBNAME,USER,PWD = "5439", "db", "wealthfront", "Wealthfront1";
    conn_string = "postgresql://" + USER + ":" + PWD + "@"+HOST+":"+ PORT + "/"+DBNAME;

    #get code from sql and clean it
    # data = clean_data(read_csv("input/loan_data.csv"));
    data = clean_data(read_sql_table("loan_data", create_engine(conn_string)));

    print "\nData pulled and cleaned! Running Our Algorthims now\n"

    #predictors is the list of fields that we will be running our algorithms on
    predictors = numerical

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

    #lets run our algos!
    for alg in algos :
        create_submission(alg[0], alg[2],data, predictors, alg[1]+".csv")

    print "\nEND\n"




if __name__ == '__main__':
    main()
