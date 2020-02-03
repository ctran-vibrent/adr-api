import mysql.connector as mysql
from twilio.rest import Client
import os
#
db = os.environ['DATABASE']
db_user = os.environ['USER']
db_password = os.environ['PASSWORD']
db_host = os.environ['HOST']
db_port = int(os.environ['PORT'])

#twilio
twilo_id = os.environ['TWILIO_ID']
twilio_token  = os.environ['TWILIO_TOKEN']

def mySQL_connect(*args, **kwargs):
    cnx = mysql.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database='adr')
    query = args[0]
    cur = cnx.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def twilio_connect(date_start,date_end):
    twilio_client = Client(twilo_id, twilio_token)
    return twilio_client.messages.list(date_sent_after  = date_start,
                                       date_sent_before = date_end)
