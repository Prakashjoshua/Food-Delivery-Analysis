import pandas as pd
import numpy as np

df = pd.read_csv("ONINE_FOOD_DELIVERY_ANALYSIS.csv")

print("Original Shape:", df.shape)

df.drop_duplicates(inplace=True)
print("After Removing Duplicates:", df.shape)

num_cols = df.select_dtypes(include=["int64", "float64"]).columns

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

cat_cols = df.select_dtypes(include="object").columns

for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("Missing values handled")

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

df["Order_Time"] = pd.to_datetime(df["Order_Time"], errors="coerce")

df["Peak_Hour"] = df["Peak_Hour"].astype(bool)

print("Data types corrected")

df = df[df["Delivery_Rating"] <= 5]

df = df[df["Delivery_Time_Min"] > 0]

df = df[df["Order_Value"] > 0]

df = df[df["Profit_Margin"] >= 0]

print("Invalid values removed")

def cap_outliers(column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[column] = df[column].clip(lower, upper)

cap_outliers("Order_Value")
cap_outliers("Delivery_Time_Min")
cap_outliers("Distance_km")

print("Outliers capped")

df.loc[df["Order_Status"] == "Cancelled", "Delivery_Rating"] = np.nan

df.loc[df["Order_Status"] == "Delivered", "Cancellation_Reason"] = np.nan

print("Logical consistency applied")

df["Profit_Percentage"] = df["Profit_Margin"] * 100

df["Order_Hour"] = df["Order_Time"].dt.hour

df["Day_Type"] = df["Order_Date"].dt.dayofweek.apply(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

print("New features created")

df.to_csv("ONLINE_FOOD_DELIVERY_CLEANED.csv", index=False)

print("✅ Cleaning Completed Successfully")
print("Final Shape:", df.shape)
