Select addr_state,COUNT(*),AVG(annual_inc) AS avg_annual_inc from loan_data
GROUP BY addr_state
ORDER BY COUNT(*) DESC
LIMIT 10;