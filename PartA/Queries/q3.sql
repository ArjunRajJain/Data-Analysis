with 
	stateData as
	(Select addr_state, COUNT(id) AS num_customers
	FROM loan_data
	GROUP BY addr_state),
	percentiles as 
	(SELECT l.addr_state,l.loan_amnt, num_customers,ntile(100) over (order by loan_amnt) AS percentile
	FROM loan_data l
	JOIN stateData s 
	ON l.addr_state = s.addr_state)

Select addr_state,avg(loan_amnt) as amnt, AVG(num_customers) as num
From percentiles
Where percentile = 90
Group by addr_state
ORDER BY amnt, num DESC
LIMIT 10