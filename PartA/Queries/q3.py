#!/usr/bin/python
import psycopg2
import sys

#set up variables
HOST = "'sql-exercise.cnfbdodh0lq8.us-west-2.redshift.amazonaws.com'";
PORT =  "'5439'"
DBNAME = "'db'"
USER = "'wealthfront'"
PWD = "'Wealthfront1'"

#Connect to RedShift
conn_string = "dbname="+DBNAME + "port=" + PORT + " user=" + USER + " password=" + PWD + " host= " + HOST;
print "Connecting to database\n        ->%s" % (conn_string)
conn = psycopg2.connect(conn_string);

cursor = conn.cursor();

results = [];

# get the countries first
cursor.execute("""
Select addr_state, COUNT(id) AS num_customers
FROM loan_data
GROUP BY addr_state
""");


# iterate through each country and get the appropriate percentile amount
for result in cursor.fetchall():
    #ntile is assigning percentiles to the appropriate row based on the order of loan_amnt
    #after we assign it, we simply find the ones that have a 90th percentile (top 10%)
    #and average them up to get the appropriate loan amount at the top 10%.
    str = """
    with percentiles as
	(SELECT loan_amnt, ntile(100) over (order by loan_amnt) AS percentile
	FROM loan_data
	WHERE addr_state = """;
    str+= "'"+result[0] + "')\n";
    str+= """
        Select avg(loan_amnt) as top_loan_amnt
        From percentiles
        Where percentile = 90;
    """;
    cursor.execute(str);
    temp = cursor.fetchall();
    results.append((result[0],temp[0][0],result[1]));

# print top 10
# we sort first on the loan_amnt and then the num_customers
i = 0;
for result in sorted(sorted(results, key=lambda x:x[2],reverse=True),key=lambda x:x[1],reverse=True):
    if(i < 10) :
        i += 1;
        print result[0], result[1], result[2];
    else :
        break;


conn.commit();
conn.close();
