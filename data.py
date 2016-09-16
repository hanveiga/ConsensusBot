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
            self.list_of_negative_times = []

    def parse_text(self, message_text):
        return message_text.split('.')

    def get_times(self):
        m = mp.MessageParser()
        return [m.extract_datetime_range(string) for string in self.parsed]
