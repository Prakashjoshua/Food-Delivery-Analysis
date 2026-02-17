import streamlit as st
import pandas as pd
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jcap@88703",
        database="guvi_project_02"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Online Food Delivery Analysis", layout="wide")
st.title("🍔 Online Food Delivery - 15 Analytical Tasks")

tasks = {
    "1. Top Spending Customers": """
        SELECT Customer_ID, SUM(Order_Value) AS Total_Spent
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Customer_ID
        ORDER BY Total_Spent DESC
        LIMIT 10;
    """,

    "2. Age Group vs Order Value": """
        SELECT Customer_Age, AVG(Order_Value) AS Avg_Order_Value
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Customer_Age
        ORDER BY Avg_Order_Value DESC
        LIMIT 10;
    """,

    "3. Weekend vs Weekday Orders": """
        SELECT Day_Type, COUNT(Order_ID) AS Total_Orders
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Day_Type
        LIMIT 10;
    """,

    "4. Monthly Revenue Trend": """
        SELECT MONTH(Order_Date) AS Month,
               SUM(Order_Value) AS Monthly_Revenue
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Month
        ORDER BY Month
        LIMIT 10;
    """,

    "5. Discount Impact on Profit": """
        SELECT Discount_Applied,
               AVG(Profit_Margin) AS Avg_Profit
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Discount_Applied
        LIMIT 10;
    """,

    "6. High Revenue Cities": """
        SELECT City,
               SUM(Order_Value) AS Total_Revenue
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY City
        ORDER BY Total_Revenue DESC
        LIMIT 10;
    """,

    "7. Average Delivery Time by City": """
        SELECT City,
               AVG(Delivery_Time_Min) AS Avg_Delivery_Time
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY City
        ORDER BY Avg_Delivery_Time DESC
        LIMIT 10;
    """,

    "8. Distance vs Delivery Delay": """
        SELECT Distance_km,
               Delivery_Time_Min
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        ORDER BY Delivery_Time_Min DESC
        LIMIT 10;
    """,

    "9. Delivery Rating vs Delivery Time": """
        SELECT Delivery_Rating,
               AVG(Delivery_Time_Min) AS Avg_Time
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Delivery_Rating
        LIMIT 10;
    """,

    "10. Top Rated Restaurants": """
        SELECT Restaurant_Name,
               AVG(Restaurant_Rating) AS Avg_Rating
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Restaurant_Name
        ORDER BY Avg_Rating DESC
        LIMIT 10;
    """,

    "11. Cancellation Rate by Restaurant": """
        SELECT Restaurant_Name,
               COUNT(*) AS Cancel_Count
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        WHERE Order_Status = 'Cancelled'
        GROUP BY Restaurant_Name
        ORDER BY Cancel_Count DESC
        LIMIT 10;
    """,

    "12. Cuisine-wise Performance": """
        SELECT Cuisine_Type,
               SUM(Order_Value) AS Total_Revenue
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Cuisine_Type
        ORDER BY Total_Revenue DESC
        LIMIT 10;
    """,

    "13. Peak Hour Demand": """
        SELECT Order_Hour,
               COUNT(Order_ID) AS Total_Orders
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Order_Hour
        ORDER BY Total_Orders DESC
        LIMIT 10;
    """,

    "14. Payment Mode Preferences": """
        SELECT Payment_Mode,
               COUNT(Order_ID) AS Usage_Count
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        GROUP BY Payment_Mode
        ORDER BY Usage_Count DESC
        LIMIT 10;
    """,

    "15. Cancellation Reason Analysis": """
        SELECT Cancellation_Reason,
               COUNT(Order_ID) AS Total_Cancellations
        FROM ONLINE_FOOD_DELIVERY_CLEANED
        WHERE Order_Status = 'Cancelled'
        GROUP BY Cancellation_Reason
        ORDER BY Total_Cancellations DESC
        LIMIT 10;
    """
}

selected_task = st.selectbox("Select a Question", list(tasks.keys()))

query = tasks[selected_task]

st.subheader("SQL Query")
st.code(query, language="sql")

st.subheader("Output (Top 10 Rows)")
df = run_query(query)
st.dataframe(df)
