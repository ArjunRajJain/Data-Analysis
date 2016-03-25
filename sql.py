
#!/usr/bin/python
import psycopg2
import sys
import pprint
from datetime import date, timedelta

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

#Captures Column Names
column_names = [];
cursor.execute("Select * from loan_data limit 5;");
for result in cursor.fetchall():
    id, loan_amnt, funded_amnt, term, int_rate, installment, emp_length, home_ownership, annual_inc, loan_status, purpose, addr_state, dti, delinq_2yrs, earliest_cr_line, mths_since_last_delinq, open_acc, revol_bal, total_acc, out_prncp, total_pymnt, total_rec_prncp, total_rec_int, wtd_loans, interest_rate, int_rate2, num_rate, numrate

#NR for this - argument under timedelta can be taken as  int(str(sys.argv[1]))
yest = date.today() - timedelta(1);
yest_str= yest.strftime('%Y-%m-%d');
print "Yesterday was\n        ->%s" % (yest_str)

conn.commit();
conn.close();
