import re
import parsing.MessageParser as mp

class DataMessage:

    def __init__(self, user=None, message=None,testing=False,**kwargs):

        if testing:
            setattr(self, 'user', kwargs.get('user_e', None))
            setattr(self, 'created_at', kwargs.get('created_at', None))
            setattr(self, 'parsed', self.parse_text(kwargs.get('message_e', None)))
            setattr(self, 'list_of_times', self.get_times())
        else:
            self.user = user.id
            self.created_at = message.date
            self.parsed = self.parse_text(message.text)
            self.list_of_times = self.get_times()



    def parse_text(self,message_text):
        list_text = message_text.split('.')
        #print list_text
        return list_text

    def get_times(self):
        m = mp.MessageParser()
        list_of_times = []
        for string in self.parsed:
            try:
                list_of_times.append(m.extract_datetime_range(string))
            except:
                continue
        return list_of_times