import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("ONLINE_FOOD_DELIVERY_CLEANED.csv")

print("CSV Loaded Successfully")
print("Total rows in CSV:", len(df))

engine = create_engine(
    "mysql+mysqlconnector://root:Jcap%4088703@127.0.0.1:3306/guvi_project_02",
    connect_args={
        "auth_plugin": "mysql_native_password",
        "use_pure": True
    }
)

print("Connected to MySQL Successfully")

df.to_sql(
    name="orders",
    con=engine,
    if_exists="replace", 
    index=False
)

print("All data inserted successfully!")
