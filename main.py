import smtplib
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
api_key = os.environ["api_key"]
account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]
from_num = "+16204496534"


my_email = "ituairegbeyanose@gmail.com"
password = os.environ["email_password"]

# MY_LAT = 6.687590
# MY_LONG = 3.234390
MY_LAT = 9.082320
MY_LONG = 6.000030

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}
hourly_weather = []
weather_id_codes = []
rain_likely_hood = 0

response = requests.get(url="https://api.openweathermap.org/data/3.0/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()["hourly"]
weather_data = weather_data[0:12]

for i in range(12):
    hourly_weather.append(weather_data[i]["weather"])

for item in hourly_weather:
    for values in item:
        weather_id_codes.append(values["id"])

for code in weather_id_codes:
    if int(code) < 700:
        rain_likely_hood = 1


if rain_likely_hood:
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {"https": os.environ['https_proxy']}
    # client = Client(account_sid,auth_token, http_client=proxy_client)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Get prepared i fore see a storm coming",
        from_=f"{from_num}",
        to="+2348125691094"
    )
    print(message.status)
    print(message.sid)
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
        connection.login(my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="ituadavid200527@gmail.com",
                            msg="Subject: Weather Forecast\n\n Hey David! It might be a good idea to take an umbrella."
                                "Get prepared it is going to rain")

