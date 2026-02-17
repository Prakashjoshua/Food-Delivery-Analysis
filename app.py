import streamlit as st
import pandas as pd

st.set_page_config(page_title="Food Delivery Analysis", layout="wide")
st.title("🍔 Online Food Delivery - 15 Analytical Tasks")

@st.cache_data
def load_data():
    return pd.read_csv("ONLINE_FOOD_DELIVERY_CLEANED.csv")

df = load_data()


task = st.selectbox("Select a Question", [

"1. Top Spending Customers",
"2. Age Group vs Order Value",
"3. Weekend vs Weekday Orders",
"4. Monthly Revenue Trend",
"5. Discount Impact on Profit",
"6. High Revenue Cities",
"7. Average Delivery Time by City",
"8. Distance vs Delivery Delay",
"9. Delivery Rating vs Delivery Time",
"10. Top Rated Restaurants",
"11. Cancellation Rate by Restaurant",
"12. Cuisine-wise Performance",
"13. Peak Hour Demand",
"14. Payment Mode Preferences",
"15. Cancellation Reason Analysis"
])


if task == "1. Top Spending Customers":

    query = """
    SELECT Customer_ID, SUM(Order_Value) AS Total_Spent
    FROM orders
    GROUP BY Customer_ID
    ORDER BY Total_Spent DESC
    LIMIT 10;
    """

    result = (
        df.groupby("Customer_ID")["Order_Value"]
        .sum()
        .reset_index()
        .sort_values(by="Order_Value", ascending=False)
        .head(10)
    )

elif task == "2. Age Group vs Order Value":

    query = """
    SELECT Customer_Age, AVG(Order_Value)
    FROM orders
    GROUP BY Customer_Age
    LIMIT 10;
    """

    result = (
        df.groupby("Customer_Age")["Order_Value"]
        .mean()
        .reset_index()
        .sort_values(by="Order_Value", ascending=False)
        .head(10)
    )

elif task == "3. Weekend vs Weekday Orders":

    query = """
    SELECT Day_Type, COUNT(Order_ID)
    FROM orders
    GROUP BY Day_Type;
    """

    result = (
        df.groupby("Day_Type")["Order_ID"]
        .count()
        .reset_index()
    )

elif task == "4. Monthly Revenue Trend":

    query = """
    SELECT MONTH(Order_Date), SUM(Order_Value)
    FROM orders
    GROUP BY MONTH(Order_Date)
    LIMIT 10;
    """

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    result = (
        df.groupby("Month")["Order_Value"]
        .sum()
        .reset_index()
        .sort_values(by="Month")
        .head(10)
    )

elif task == "5. Discount Impact on Profit":

    query = """
    SELECT Discount_Applied, AVG(Profit_Margin)
    FROM orders
    GROUP BY Discount_Applied
    LIMIT 10;
    """

    result = (
        df.groupby("Discount_Applied")["Profit_Margin"]
        .mean()
        .reset_index()
        .head(10)
    )

elif task == "6. High Revenue Cities":

    query = """
    SELECT City, SUM(Order_Value)
    FROM orders
    GROUP BY City
    ORDER BY SUM(Order_Value) DESC
    LIMIT 10;
    """

    result = (
        df.groupby("City")["Order_Value"]
        .sum()
        .reset_index()
        .sort_values(by="Order_Value", ascending=False)
        .head(10)
    )

elif task == "7. Average Delivery Time by City":

    query = """
    SELECT City, AVG(Delivery_Time_Min)
    FROM orders
    GROUP BY City
    LIMIT 10;
    """

    result = (
        df.groupby("City")["Delivery_Time_Min"]
        .mean()
        .reset_index()
        .head(10)
    )

elif task == "8. Distance vs Delivery Delay":

    query = """
    SELECT Distance_km, Delivery_Time_Min
    FROM orders
    LIMIT 10;
    """

    result = df[["Distance_km", "Delivery_Time_Min"]].head(10)

elif task == "9. Delivery Rating vs Delivery Time":

    query = """
    SELECT Delivery_Rating, AVG(Delivery_Time_Min)
    FROM orders
    GROUP BY Delivery_Rating
    LIMIT 10;
    """

    result = (
        df.groupby("Delivery_Rating")["Delivery_Time_Min"]
        .mean()
        .reset_index()
        .head(10)
    )

elif task == "10. Top Rated Restaurants":

    query = """
    SELECT Restaurant_Name, AVG(Restaurant_Rating)
    FROM orders
    GROUP BY Restaurant_Name
    ORDER BY AVG(Restaurant_Rating) DESC
    LIMIT 10;
    """

    result = (
        df.groupby("Restaurant_Name")["Restaurant_Rating"]
        .mean()
        .reset_index()
        .sort_values(by="Restaurant_Rating", ascending=False)
        .head(10)
    )

elif task == "11. Cancellation Rate by Restaurant":

    query = """
    SELECT Restaurant_Name, COUNT(*)
    FROM orders
    WHERE Order_Status = 'Cancelled'
    GROUP BY Restaurant_Name
    LIMIT 10;
    """

    result = (
        df[df["Order_Status"] == "Cancelled"]
        .groupby("Restaurant_Name")["Order_ID"]
        .count()
        .reset_index()
        .head(10)
    )

elif task == "12. Cuisine-wise Performance":

    query = """
    SELECT Cuisine_Type, SUM(Order_Value)
    FROM orders
    GROUP BY Cuisine_Type
    LIMIT 10;
    """

    result = (
        df.groupby("Cuisine_Type")["Order_Value"]
        .sum()
        .reset_index()
        .sort_values(by="Order_Value", ascending=False)
        .head(10)
    )

elif task == "13. Peak Hour Demand":

    query = """
    SELECT Order_Hour, COUNT(Order_ID)
    FROM orders
    GROUP BY Order_Hour
    LIMIT 10;
    """

    result = (
        df.groupby("Order_Hour")["Order_ID"]
        .count()
        .reset_index()
        .sort_values(by="Order_ID", ascending=False)
        .head(10)
    )

elif task == "14. Payment Mode Preferences":

    query = """
    SELECT Payment_Mode, COUNT(Order_ID)
    FROM orders
    GROUP BY Payment_Mode
    LIMIT 10;
    """

    result = (
        df.groupby("Payment_Mode")["Order_ID"]
        .count()
        .reset_index()
        .sort_values(by="Order_ID", ascending=False)
        .head(10)
    )

elif task == "15. Cancellation Reason Analysis":

    query = """
    SELECT Cancellation_Reason, COUNT(Order_ID)
    FROM orders
    WHERE Order_Status = 'Cancelled'
    GROUP BY Cancellation_Reason
    LIMIT 10;
    """

    result = (
        df[df["Order_Status"] == "Cancelled"]
        .groupby("Cancellation_Reason")["Order_ID"]
        .count()
        .reset_index()
        .sort_values(by="Order_ID", ascending=False)
        .head(10)
    )



st.subheader("SQL Query")
st.code(query, language="sql")

st.subheader("Output (Top 10 Rows)")
st.dataframe(result)
