#!/usr/bin/python
import psycopg2
import sys
import pandas

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

result = pandas.read_sql_table("loan_data", conn);
print result;


conn.commit();
conn.close();
