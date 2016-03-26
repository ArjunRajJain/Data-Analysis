Select 
	addr_state,
	COUNT(id) AS num_customers,
	AVG(annual_inc) AS avg_annual_inc 
FROM loan_data
GROUP BY addr_state
ORDER BY COUNT(id) DESC
LIMIT 10;