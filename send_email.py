import os
import csv
import smtplib
import psycopg2
from email.message import EmailMessage

# Database connection info from GitHub Secrets
DB_HOST = os.getenv("SUPABASE_HOST")
DB_NAME = os.getenv("SUPABASE_DB")
DB_USER = os.getenv("SUPABASE_USER")
DB_PASS = os.getenv("SUPABASE_PASSWORD")

# Gmail info from GitHub Secrets
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def fetch_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode='require'
    )

    cursor = conn.cursor()
    with open("query.sql", "r") as f:
        query = f.read()

    cursor.execute(query)
    rows = cursor.fetchall()

    # Write CSV
    with open("DailySalesReport.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["SaleID", "SaleDate", "CustomerName", "ProductName", "Quantity", "UnitPrice", "TotalAmount"])
        writer.writerows(rows)

    cursor.close()
    conn.close()

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Daily Sales Report"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content("Attached is today's sales report.")

    with open("DailySalesReport.csv", "rb") as f:
        msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="DailySalesReport.csv")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    fetch_data()
    send_email()
