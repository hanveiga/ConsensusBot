from wit import Wit
import json
from dateutil import parser
from datetime import timedelta

ACCESSTOKEN = 'I2XMHO2GC4SYR4GYO4ZG7732JXIG34XF'


class MessageParser():
    def __init__(self):
        self.client = Wit(access_token= ACCESSTOKEN)

    def extract_datetime_range(self,message):
        resp = self.client.message(message)
        resp = json.loads(str(resp).replace("u'","'").replace("'",'"'))
        isnegative  = False
        if "negative" in resp['entities']:
            isnegative = True
        resp = resp['entities']['datetime'][0]
        if resp['type'] == 'interval':
            return parser.parse(resp['from']['value']) ,parser.parse(resp['to']['value'])
        else:
            datefrom = parser.parse(resp['value'])
            if resp['grain'] == 'hour':
                dateto = datefrom +timedelta(hours=1)
            if resp['grain'] == 'day':
                dateto = datefrom +timedelta(days=1)
            if resp['grain'] == 'week':
                dateto = datefrom +timedelta(days=7)
            if resp['grain'] == 'month':
                dateto = datefrom +timedelta(days=30)
            return datefrom,dateto,isnegative

    def extract_intent(self,message):
        resp = self.client.message(message)
        resp = json.loads(str(resp).replace("u'","'").replace("'",'"'))
        resp = resp['entities']
        if "start" in resp:
            return "start"
        elif "end" in resp:
            return "end"
        elif "datetime" in resp:
            return "times"
        else:
            return "None"

#m = MessageParser()
#print m.extract_datetime_range('i can do it on friday')


