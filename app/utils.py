from app.database import *
from user_agents import parse as agent_parse
import datetime
import json

def parse_agents(rows):
    for r in rows:
        user_agent = dict(
            user_agent=dict(),
            count=r[1]
        )
        if r[0] is None:
            user_agent['user_agent']['device'] = 'Unknown device'
        else:
            u_agent = agent_parse(r[0])
            user_agent['user_agent']['device'] = str(u_agent)
        for k in ['is_mobile','is_tablet',
                    'is_touch_capable', 'is_pc', 'is_bot']:
            user_agent['user_agent'][k] = False if r[0] is None else getattr(u_agent,k)
        yield user_agent

def get_click_user_agents(past_days):
    query='''SELECT click_useragent ,
            	   COUNT(*) as count
             FROM email_detail
             where send_mail_timestamp >= (CURDATE() - INTERVAL %d DAY )
             group by click_useragent
             order by count desc;''' % (past_days)
    results = [u_agent for u_agent in parse_agents(mySQL_connect(query))]
    return results

def get_open_user_agents(past_days):
    query='''SELECT open_useragent ,
            	   COUNT(*) as count
             FROM email_detail
             where send_mail_timestamp >= (CURDATE() - INTERVAL %d DAY )
             group by open_useragent
             order by count desc;''' % (past_days)
    results = [u_agent for u_agent in parse_agents(mySQL_connect(query))]
    return results

def get_click_links(past_days):
    query='''SELECT click_link,
            		COUNT(*) as count
            FROM email_detail
            WHERE
            	click_link IS NOT NULL
            AND send_mail_timestamp >= (CURDATE() - INTERVAL %d DAY )
            GROUP BY click_link
            ORDER BY count desc;''' % (past_days)
    results = []
    for r in  mySQL_connect(query):
        link = dict(
            click_link='',
            count=r[1]
        )
        link['click_link'] = r[0] if r[0] is not None \
                            else 'Unknown'
        results.append(link)
    return results

def datetime_serializer(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def get_twilio_by_days(past_days):
    today = datetime.datetime.now()
    dt_end = datetime.datetime(today.year, today.month, today.day, 0, 0)
    dt_start = dt_end - datetime.timedelta(days=past_days)
    messages = twilio_connect(dt_start, dt_end)
    return json.dumps([{'twilio_account_sid' : r.account_sid,
                'sms_message_body' : r.body,
                'sms_date_sent' : r.date_sent,
                'direction' : r.direction,
                'error_code' : r.error_code,
                'sender_number' : r.from_,
                'messaging_service_sid' : r.messaging_service_sid,
                'status' : r.status,
                'twilio_sms_sid' : r.sid,
                'recipient_number' : r.to
                } for r in messages]
                , default = datetime_serializer)

def persist_twilio(messages):
    table = 'sms_twilio'
    columns = messages[0].keys()
    data = [(val for val in row.values()) for row in messages]
    mySQL_batch_ingest(table, columns, data)
    return {'Success': True }
