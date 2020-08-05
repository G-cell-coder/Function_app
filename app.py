from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import pandas as pd
from twilio.rest import Client
import conf
import time as t
from flask import Flask
import math
import datetime
from datetime import timedelta
#app = Flask(__name__)


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Time-keeper').sheet1

pp = pprint.PrettyPrinter()
data = sheet.get_all_values()
column = data[0]
col_di = {}

for i,j in zip(range(0,len(column)),column):
	col_di[i]=j

df = pd.DataFrame(data)
df.set_index(0, inplace=True)
df = df.transpose()
df.set_index(['Name'], inplace= True)
df = df.T
print(len(df))


@app.route('/')
def execute():
        for i in range(2,len(df)+2):
                print(df.iloc[i-2,0],sheet.cell(i,7).value, sheet.cell(i,5).value)
                if (sheet.cell(i,5).value != "TIMEOUT") & (sheet.cell(i,7).value != "0:00:00"):
                        print("SENDING SMS")
                        client.messages.create(to=df.iloc[i-2,0],
                                           from_="<TWILIO MOBILE NUMBER>",
                                           body="Penalty of "+sheet.cell(i,9).value+" should be paid while billing")
                        sheet.update_cell(i,5, "TIMEOUT")
                        i= i +1

                else:
                        i= i+1
                        print("SMS NOT SENT")

                continue

#CODE SNIPPET TO HANDLE THE INCOMMING SMS ON EXTENTION
if __name__ == "__main__":
#        app.run()
        client = Client("<TWILIO ACCOUNT ID>", "<AUTH TOKEN>")
        execute()






    






