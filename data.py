import re
import parsing.MessageParser as mp

class DataMessage:

    __slots__ = ('user', 'raw_text', 'created_at', 'list_of_times')

    def __init__(self, user, message):
        self.user = user.id
        #self.raw_text = message.text
        self.created_at = message.date
        self.parsed = self.parse_text(message.text)
        self.list_of_times = self.get_times()

    def parse_text(self,message_text):
        list_text = message_text.split('.')
        print list_text
        return list_text

    def get_times(self):
        m = mp.MessageParser()
        list_of_times = [m.extract_datetime_range(string) for string in self.parsed]
        return list_of_times