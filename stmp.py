import datetime as dt
import smtplib
import random

MY_EMAIL = "breezeshawl@gmail.com"
PASS = "03148520kK"

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 2:
    with open("qoutes.txt") as qoutes_file:
        all_qoutes = qoutes_file.readlines()
        quote = random.choice(all_qoutes)

    print(quote)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Today Motivation\n\n{quote}"
        )

#Monday Motivation Project
# import smtplib
# import datetime as dt
# import random

# MY_EMAIL = "appbreweryinfo@gmail.com"
# MY_PASSWORD = "abcd1234()"

# now = dt.datetime.now()
# weekday = now.weekday()
# if weekday == 1:
#     with open("quotes.txt") as quote_file:
#         all_quotes = quote_file.readlines()
#         quote = random.choice(all_quotes)

#     print(quote)
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(MY_EMAIL, MY_PASSWORD)
#         connection.sendmail(
#             from_addr=MY_EMAIL,
#             to_addrs=MY_EMAIL,
#             msg=f"Subject:Monday Motivation\n\n{quote}"
#         )