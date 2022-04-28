# To run and test the code you need to update 3 places:
# 1. Change MY_EMAIL/MY_PASSWORD/RECEIVER_EMAIL to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.

from datetime import date
from datetime import timedelta
import smtplib
import sqlite3
from portfolio import companies

today = date.today()
yesterday = today - timedelta(days=2)
day_before_yesterday = today - timedelta(days=3)

msg = []

# Get Access to Database
connection = sqlite3.connect("Stocks.db")
cursor = connection.cursor()

# For loop to check each company's Profit Or Loss
for i in companies:

    # Get Yesterday's Price from database, to match with Day before price for Loss or Profit
    cursor.execute(f"SELECT close FROM {i} WHERE time_stamp='{yesterday}'")
    yesterday_closing_price = cursor.fetchone()

    # Get Day before yesterday price from database
    cursor.execute(f"SELECT close FROM {i} WHERE time_stamp='{day_before_yesterday}'")
    day_before_yesterday_closing_price = cursor.fetchone()

    # Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
    difference = float(yesterday_closing_price[0]) - float(day_before_yesterday_closing_price[0])
    diff_percent = round((difference / float(yesterday_closing_price[0])) * 100)
    up_down = None
    if difference > 0:
        a = f"Your Shares in {i} Increased by {diff_percent}%"
        msg.append(a)
    else:
        a = f"Your Shares in {i} Decreased by {diff_percent}%"
        msg.append(a)


def send_mail(message):
    MY_EMAIL = "abdimalik.omar@chasacademy.se"
    MY_PASSWORD = "Security0303"
    RECEIVER_EMAIL = 'abdimalik.omar@chasacademy.se'
    try:
        # Create your SMTP session
        smtp = smtplib.SMTP('smtp.gmail.com', 587)

        # Use TLS to add security
        smtp.starttls()

        # User Authentication
        smtp.login(MY_EMAIL, MY_PASSWORD)

        # Sending the Email
        smtp.sendmail(MY_EMAIL, RECEIVER_EMAIL, message)

        # Terminating the session
        smtp.quit()
        print("Email sent successfully!")

    except Exception as ex:
        print("Something went wrong....", ex)


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele
        str1 += '\n'

        # return string
    return str1



send_mail(listToString(msg))
