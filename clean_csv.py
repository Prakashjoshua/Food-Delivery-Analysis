import pandas as pd
import numpy as np

# -------------------------------------------------
# STEP 1: LOAD DATA
# -------------------------------------------------

df = pd.read_csv("ONINE_FOOD_DELIVERY_ANALYSIS.csv")

print("Original Shape:", df.shape)


# -------------------------------------------------
# STEP 2: REMOVE DUPLICATES
# -------------------------------------------------

df.drop_duplicates(inplace=True)
print("After Removing Duplicates:", df.shape)


# -------------------------------------------------
# STEP 3: HANDLE MISSING VALUES
# -------------------------------------------------

# 3.1 Numerical Columns → Fill with Median
num_cols = df.select_dtypes(include=["int64", "float64"]).columns

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# 3.2 Categorical Columns → Fill with Mode
cat_cols = df.select_dtypes(include="object").columns

for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("Missing values handled")


# -------------------------------------------------
# STEP 4: DATA TYPE CORRECTION
# -------------------------------------------------

# Convert Order_Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Convert Order_Time to datetime
df["Order_Time"] = pd.to_datetime(df["Order_Time"], errors="coerce")

# Convert Peak_Hour to boolean
df["Peak_Hour"] = df["Peak_Hour"].astype(bool)

print("Data types corrected")


# -------------------------------------------------
# STEP 5: REMOVE INVALID VALUES
# -------------------------------------------------

# Delivery rating should not exceed 5
df = df[df["Delivery_Rating"] <= 5]

# Delivery time must be positive
df = df[df["Delivery_Time_Min"] > 0]

# Order value must be positive
df = df[df["Order_Value"] > 0]

# Profit margin must be positive
df = df[df["Profit_Margin"] >= 0]

print("Invalid values removed")


# -------------------------------------------------
# STEP 6: OUTLIER TREATMENT (IQR METHOD)
# -------------------------------------------------

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


# -------------------------------------------------
# STEP 7: LOGICAL CONSISTENCY FIX
# -------------------------------------------------

# Cancelled orders should not have Delivery Rating
df.loc[df["Order_Status"] == "Cancelled", "Delivery_Rating"] = np.nan

# Delivered orders should not have Cancellation Reason
df.loc[df["Order_Status"] == "Delivered", "Cancellation_Reason"] = np.nan

print("Logical consistency applied")


# -------------------------------------------------
# STEP 8: CREATE CLEAN FEATURES
# -------------------------------------------------

# Create Profit Percentage
df["Profit_Percentage"] = df["Profit_Margin"] * 100

# Create Order Hour
df["Order_Hour"] = df["Order_Time"].dt.hour

# Create Day Type (Weekday / Weekend)
df["Day_Type"] = df["Order_Date"].dt.dayofweek.apply(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

print("New features created")


# -------------------------------------------------
# STEP 9: SAVE CLEANED DATA
# -------------------------------------------------

df.to_csv("ONLINE_FOOD_DELIVERY_CLEANED.csv", index=False)

print("✅ Cleaning Completed Successfully")
print("Final Shape:", df.shape)
