-- 1. Total amount spent per category
SELECT Category, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY Category;

-- 2. Monthly spending trends
SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS Monthly_Spent
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 3. Total amount spent using each PaymentMode
SELECT PaymentMode, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY PaymentMode;

-- 4. Average transaction amount by category
SELECT Category, AVG(AmountPaid) AS Avg_Spent
FROM expenses
GROUP BY Category;

-- 5. Number of transactions per category
SELECT Category, COUNT(*) AS Transaction_Count
FROM expenses
GROUP BY Category;

-- 6. Daily spending trends
SELECT Date, SUM(AmountPaid) AS Daily_Spent
FROM expenses
GROUP BY Date
ORDER BY Date;

-- 7. Categories with more than 100 transactions
SELECT Category, COUNT(*) AS Transaction_Count
FROM expenses
GROUP BY Category
HAVING Transaction_Count > 100;

-- 8. Days with highest spending
SELECT Date, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY Date
ORDER BY Total_Spent DESC
LIMIT 5;

-- 9. Total amount spent on "Groceries"
SELECT SUM(AmountPaid) AS Total_Spent
FROM expenses
WHERE Category = 'Groceries';

-- 10. Monthly cashback trends
SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Cashback) AS Monthly_Cashback
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 11. Highest spending day per category
SELECT Category, Date, MAX(AmountPaid) AS Max_Spent
FROM expenses
GROUP BY Category, Date;

-- 12. Average spending per transaction by PaymentMode
SELECT PaymentMode, AVG(AmountPaid) AS Avg_Spent
FROM expenses
GROUP BY PaymentMode;

-- 13. Transactions above average spending
WITH Avg_Spent AS (
    SELECT AVG(AmountPaid) AS Avg_Amount
    FROM expenses
)
SELECT *
FROM expenses, Avg_Spent
WHERE expenses.AmountPaid > Avg_Spent.Avg_Amount;

-- 14. Day-wise average spending
SELECT Date, AVG(AmountPaid) AS Avg_Spent
FROM expenses
GROUP BY Date;

-- 15. PaymentMode with maximum transactions
SELECT PaymentMode, COUNT(*) AS Transaction_Count
FROM expenses
GROUP BY PaymentMode
ORDER BY Transaction_Count DESC
LIMIT 1;

-- 16. Categories with spending exceeding $10,000
SELECT Category, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY Category
HAVING Total_Spent > 10000;

-- 17. Total cashback earned on "Shopping"
SELECT SUM(Cashback) AS Total_Cashback
FROM expenses
WHERE Category = 'Shopping';

-- 18. Spending trends by PaymentMode and category
SELECT PaymentMode, Category, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY PaymentMode, Category;

-- 19. Monthly percentage contribution of each category to total spending
WITH Monthly_Spend AS (
    SELECT 
        DATE_FORMAT(Date, '%Y-%m') AS Month,
        Category,
        SUM(AmountPaid) AS Category_Spent,
        SUM(SUM(AmountPaid)) OVER (PARTITION BY DATE_FORMAT(Date, '%Y-%m')) AS Total_Spent
    FROM expenses
    GROUP BY Month, Category
)
SELECT 
    Month,
    Category,
    (Category_Spent * 100.0 / Total_Spent) AS Percentage_Contribution
FROM Monthly_Spend
ORDER BY Month, Percentage_Contribution DESC;

-- 20. Trend analysis: Increase or decrease in monthly spending
WITH Monthly_Spend AS (
    SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS Total_Spent
    FROM expenses
    GROUP BY Month
)
SELECT 
    m1.Month AS Current_Month,
    m1.Total_Spent AS Current_Spent,
    m2.Total_Spent AS Previous_Spent,
    (m1.Total_Spent - m2.Total_Spent) AS Spending_Change
FROM Monthly_Spend m1
LEFT JOIN Monthly_Spend m2 
    ON DATE_ADD(STR_TO_DATE(CONCAT(m1.Month, '-01'), '%Y-%m-%d'), INTERVAL -1 MONTH) = STR_TO_DATE(CONCAT(m2.Month, '-01'), '%Y-%m-%d');


-- 21. Seasonal spending trends (quarterly analysis)
SELECT CASE 
           WHEN MONTH(Date) IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH(Date) IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH(Date) IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       Category, SUM(AmountPaid) AS Total_Spent
FROM expenses
GROUP BY Quarter, Category;

-- 22. Ratio of cashback to total spending by month
SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, 
       SUM(Cashback) AS Total_Cashback, SUM(AmountPaid) AS Total_Spending,
       (SUM(Cashback) * 1.0 / SUM(AmountPaid)) AS Cashback_Ratio
FROM expenses
GROUP BY Month;
