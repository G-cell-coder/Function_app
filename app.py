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

df = pd.DataFrame(data[1:])
df = df.rename(columns=col_di)
df.set_index(['Name'], inplace= True)
print(df)

def stopwatch(r,sec):
	while sec:
		minn, secc = divmod(sec, 60)
		timeformat = '00:{:02d}:{:02d}'.format(minn, secc)
		sheet.update_cell(r,6,timeformat)
		print(timeformat, end='\r')
		t.sleep(1)
		sec -= 1
	
#@app.route("/")
def execute():
	i = 2
	print("INSIDE EXECUTE")
	n = 2
	while n < (len(df)+2):
		print(sheet.cell(n,6).value)
		if (sheet.cell(n,6).value == "00:00:01"):
			print(df.iloc[n-2,0])
			print("Sending SMS the data:{} and for User {}".format(sheet.cell(n,11).value,df.iloc[n-2]))
			sheet.update_cell(n,6, "TIMEOUT")
			timestamp = sheet.cell(n,8).value
			hh, mm , ss = map(int, timestamp.split(':'))
			tt= ss + 60*(mm + 60*hh)
			pay = tt * 0.50
			print("PAY FOR THE TIME(Secs):{} and TOTAL:{}".format(tt,pay))
			n = n + 1
			continue
		else:
			n = n+1
			continue

"""
#			client = Client("AC887b04f4086795cf565f1caa8e177af8", "d4ac1ba3f982fc1b5756ac48b6406ce5")		
#			client.messages.create(to=df.iloc[n-2,0],
#		                       from_="14692029195",
#	               		       body=sheet.cell(n,11).value)
			n= n + 1
			continue
		
		else:
			n = n +1
			continue




def calculate_pay(uh,um, us, uhr):
       	hours_minutes_seconds = timedelta(hours= uh, minutes = um, seconds = us)
        time_in_decimal_format = round(uh * (1/1) + um * (1/60) + us * (1/3600),2)
       	pay = time_in_decimal_format * uhr
#	    return ("Number of Hours in decimal form: {}. Total pay: {}".format(hours_minutes_seconds, pay))
#    	    return pay        
"""




#CODE SNIPPET TO HANDLE THE INCOMMING SMS ON EXTENTION
if __name__ == "__main__":
#	app.run()	
	execute()






    






