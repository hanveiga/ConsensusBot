import re

class DataMessage(object):

    def __init__(self, a, b):
        self.user = a #user.id
        self.raw_text = a #message.text
        self.created_at = a #message.date
        #self.parsed = self.parse_text()
        self.list_of_times = a

    def parse_text(self):
        list_text = re.split(self.raw_text,'.')
        print list_text
        return list_text

    #def get_times(self):
    #    list_of_times = [parser(string) for string in self.parsed]
    #    return list_of_times