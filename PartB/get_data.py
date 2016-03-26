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

def get_connection() :
    try:
        conn = psycopg2.connect(conn_string);
        return conn;
    except Exception as err:
        print(err)


conn.commit();
conn.close();
