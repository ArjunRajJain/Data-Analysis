Select addr_state, SUM(loan_amnt) AS total_loan_amnt, COUNT(id) AS num_customers, AVG(loan_amnt) AS avg_loan_amnt, AVG(SUBSTRING(int_rate,0,len(int_rate)-1)) AS avg_int_rate  from loan_data
GROUP BY addr_state
ORDER BY SUM(loan_amnt) DESC
LIMIT 10;