import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from report import district_sum


def load_data():
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
    conn.close()

    return df

def analyze(df):

    district_sum = (
        df.groupby("district")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return district_sum

def save_report(district_sum):
    district_sum.to_csv("reports/district_report.csv")

def save_plot(district_sum):
    district_sum.plot(
        kind="bar",
    )

    plt.title("Payments by District")
    plt.tight_layout()

    plt.savefig("payments.png")
    plt.close()

def main():
    df = load_data()
    district_sum = analyze(df)

    save_report(district_sum)
    save_plot(district_sum)

    print("Report generated successfully")

if __name__ == "__main__":
    main()