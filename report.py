import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn = sqlite3.connect("data/city.db")

query = """
SELECT r.name,
       r.district,
       p.amount
FROM residents r
JOIN payments p
ON r.id = p.resident_id
"""

df = pd.read_sql_query(query, conn)

# Общий оборот
total_money = df["amount"].sum()

# Топ жителей
top_users = (
    df.groupby("name")["amount"]
      .sum()
      .sort_values(ascending=False)
      .head(3)
)

# Топ районов
top_districts = (
    df.groupby("district")["amount"]
      .sum()
      .sort_values(ascending=False)
)

top_user = (
    df.groupby("name")["amount"]
      .sum()
      .sort_values(ascending=False)
      .index[0]
)

district_sum = (
    df.groupby("district")["amount"]
      .sum()
      .sort_values(ascending=True)
)

district_sum.plot(kind="line")

plt.title("Total Payments by District")
plt.xlabel("District")
plt.ylabel("Total Payments")

plt.savefig("payments_by_district.png")
plt.show()

district_sum.to_csv("reports/district_report.csv")
district_sum.to_excel("reports/district_report.xlsx")
