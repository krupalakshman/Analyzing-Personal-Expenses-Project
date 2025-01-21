import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


# Database connection details
DB_HOST = "localhost"
DB_USER = "root"                        #replace this value with your database username
DB_PASSWORD = "123456789"               #replace this value with your database password
DB_NAME = "expensetrackerdb"            #replace this value with your database name

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("Analyzing Personal Expenses")

tab_home,tab1, tab2, tab3 = st.tabs(["Home","Data", "SQL Queries", "Visualizations"])
with tab_home:
    st.header("Welcome to the Expense Analyzer")
    st.write("This is a simple expense tracker application that allows users to track their expenses and analyze their spending habits.")
    st.write("Contents of the page:")
    st.write("1. **Data**- This tab will show all the expenses.")
    st.write("2. **SQL Queries**- This tab will show the SQL queries run by the user to analyze the data.")
    st.write("3. **Visualizations**- This tab will show the visualizations made by the user.")
    
#ALL_Data Tab
with tab1:
    data=pd.read_csv("expenses_2023.csv")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset")
        st.write(data)
    with col2:
        
        st.subheader("This is a personal expenses data for the year 2023 generated using Faker library for this project. This data is used to perform sql queries and matplotlib visualizations.")
        st.subheader(" Descriptions of the Dataset")
        st.write("**Date**: The transaction date.")
        st.write("**Category**: Type of expense (Food, Transportation, Bills, etc.).")
        st.write("**Payment Mode**: Specifies whether it was a Cash or Online transaction.")
        st.write("**Description**: Details about the expense.")
        st.write("**Amount Paid**: Total amount paid for the transaction.")
        st.write("**Cashback**: Cashback received (if any) during the transaction.")



#SQL Queries Tab
with tab2:
    queries = [
    {"title": "Total amount spent per category", 
     "query": "SELECT Category, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY Category;"},
     
    {"title": "Monthly spending trends", 
     "query": "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS Monthly_Spent FROM expenses GROUP BY Month ORDER BY Month;"},
     
    {"title": "Total amount spent using each PaymentMode", 
     "query": "SELECT PaymentMode, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY PaymentMode;"},
     
    {"title": "Average transaction amount by category", 
     "query": "SELECT Category, AVG(AmountPaid) AS Avg_Spent FROM expenses GROUP BY Category;"},
     
    {"title": "Number of transactions per category", 
     "query": "SELECT Category, COUNT(*) AS Transaction_Count FROM expenses GROUP BY Category;"},
     
    {"title": "Daily spending trends", 
     "query": "SELECT Date, SUM(AmountPaid) AS Daily_Spent FROM expenses GROUP BY Date ORDER BY Date;"},
     
    {"title": "Categories with more than 100 transactions", 
     "query": "SELECT Category, COUNT(*) AS Transaction_Count FROM expenses GROUP BY Category HAVING Transaction_Count > 100;"},
     
    {"title": "Days with highest spending", 
     "query": "SELECT Date, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY Date ORDER BY Total_Spent DESC LIMIT 5;"},
     
    {"title": "Total amount spent on 'Groceries'", 
     "query": "SELECT SUM(AmountPaid) AS Total_Spent FROM expenses WHERE Category = 'Groceries';"},
     
    {"title": "Monthly cashback trends", 
     "query": "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Cashback) AS Monthly_Cashback FROM expenses GROUP BY Month ORDER BY Month;"},
     
    {"title": "Highest spending day per category", 
     "query": "SELECT Category, Date, MAX(AmountPaid) AS Max_Spent FROM expenses GROUP BY Category, Date;"},
     
    {"title": "Average spending per transaction by PaymentMode", 
     "query": "SELECT PaymentMode, AVG(AmountPaid) AS Avg_Spent FROM expenses GROUP BY PaymentMode;"},
     
    {"title": "Transactions above average spending", 
     "query": """WITH Avg_Spent AS (
                    SELECT AVG(AmountPaid) AS Avg_Amount FROM expenses
                 )
                 SELECT * FROM expenses, Avg_Spent WHERE expenses.AmountPaid > Avg_Spent.Avg_Amount;"""},
     
    {"title": "Day-wise average spending", 
     "query": "SELECT Date, AVG(AmountPaid) AS Avg_Spent FROM expenses GROUP BY Date;"},
     
    {"title": "PaymentMode with maximum transactions", 
     "query": "SELECT PaymentMode, COUNT(*) AS Transaction_Count FROM expenses GROUP BY PaymentMode ORDER BY Transaction_Count DESC LIMIT 1;"},
     
    {"title": "Categories with spending exceeding $10,000", 
     "query": "SELECT Category, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY Category HAVING Total_Spent > 10000;"},
     
    {"title": "Total cashback earned on 'Shopping'", 
     "query": "SELECT SUM(Cashback) AS Total_Cashback FROM expenses WHERE Category = 'Shopping';"},
     
    {"title": "Spending trends by PaymentMode and category", 
     "query": "SELECT PaymentMode, Category, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY PaymentMode, Category;"},
     
    {"title": "Monthly percentage contribution of each category to total spending", 
     "query": """WITH Monthly_Spend AS (
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
                 ORDER BY Month, Percentage_Contribution DESC;"""},
     
    {"title": "Trend analysis: Increase or decrease in monthly spending", 
     "query": """WITH Monthly_Spend AS (
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
                    ON DATE_ADD(STR_TO_DATE(CONCAT(m1.Month, '-01'), '%Y-%m-%d'), INTERVAL -1 MONTH) = STR_TO_DATE(CONCAT(m2.Month, '-01'), '%Y-%m-%d');"""},
     
    {"title": "Seasonal spending trends (quarterly analysis)", 
     "query": """SELECT CASE 
                    WHEN MONTH(Date) IN (1, 2, 3) THEN 'Q1'
                    WHEN MONTH(Date) IN (4, 5, 6) THEN 'Q2'
                    WHEN MONTH(Date) IN (7, 8, 9) THEN 'Q3'
                    ELSE 'Q4'
                 END AS Quarter,
                 Category, SUM(AmountPaid) AS Total_Spent
                 FROM expenses
                 GROUP BY Quarter, Category;"""},
     
    {"title": "Ratio of cashback to total spending by month", 
     "query": """SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, 
                    SUM(Cashback) AS Total_Cashback, SUM(AmountPaid) AS Total_Spending,
                    (SUM(Cashback) * 1.0 / SUM(AmountPaid)) AS Cashback_Ratio
                 FROM expenses
                 GROUP BY Month;"""}
    ]
    st.title("Select Query to Execute")
    query_titles = [q["title"] for q in queries]
    selected_title = st.selectbox("Choose a query:", query_titles)
    
    selected_query = next(q["query"] for q in queries if q["title"] == selected_title)


    # Button to execute the query
    if st.button("Execute Query"):
        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = connection.cursor(dictionary=True)
            
            # Execute the selected query
            cursor.execute(selected_query)
            results = cursor.fetchall()

            # Convert results to Pandas DataFrame
            df = pd.DataFrame(results)
            st.write("### Query")

            st.write(selected_query)
            # Display the results
            if df.empty:
                st.warning("The query returned no results.")
            else:
                st.write("### Query Results")
                st.dataframe(df)

        except mysql.connector.Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

#Visualizations Tab
with tab3:
    st.header("Visualizations")
    
    # Creating two columns
    col1, col2 = st.columns(2)

    # 1. Bar Chart: Total expenses by category
    with col1:
        category_expenses = data.groupby('Category')['Amount Paid'].sum()
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        category_expenses.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax1)
        ax1.set_title('Total Expenses by Category', fontsize=16)
        ax1.set_xlabel('Category', fontsize=12)
        ax1.set_ylabel('Total Amount Paid', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)
        st.caption("Bar Chart: Total expenses by category")
    
    # 2. Pie Chart: Distribution of payment modes
    with col2:
        payment_mode_distribution = data['Payment Mode'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(12,6))
        payment_mode_distribution.plot(
            kind='pie',
            autopct='%1.1f%%',
            startangle=140,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
            ax=ax2
        )
        ax2.set_title('Payment Mode Distribution', fontsize=16)
        ax2.set_ylabel('')  # Hide y-label for pie chart
        st.pyplot(fig2)
        st.caption("Pie Chart: Distribution of payment modes")
    
    # 3. Stacked Bar Chart: Expenses by category and payment mode
    with col1:
        expenses_by_category_and_payment = data.pivot_table(
            index='Category', 
            columns='Payment Mode', 
            values='Amount Paid', 
            aggfunc='sum', 
            fill_value=0
        )
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        expenses_by_category_and_payment.plot(
            kind='bar', 
            stacked=True, 
            color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
            edgecolor='black',
            ax=ax3
        )
        ax3.set_title('Expenses by Category and Payment Mode', fontsize=16)
        ax3.set_xlabel('Category', fontsize=12)
        ax3.set_ylabel('Total Amount Paid', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(title='Payment Mode', fontsize=10)
        st.pyplot(fig3)
        st.caption("Stacked Bar Chart: Expenses by category and payment mode")
    
    
    # 4. Line Graph: Distribution of cashback amounts visualization for stramlit
    with col2:
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        data['Cashback'].plot(kind='line', ax=ax4)
        ax4.set_title('Distribution of Cashback Amounts', fontsize=16)
        ax4.set_xlabel('Cashback Amount', fontsize=12)
        ax4.set_ylabel('Frequency', fontsize=12)
        st.pyplot(fig4)
        st.caption("Histogram: Distribution of cashback amounts")
        
