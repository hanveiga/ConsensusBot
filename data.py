import re
import parsing.MessageParser as mp

class DataMessage:

    def __init__(self, user=None, message=None,testing=False,**kwargs):

        if testing:
            setattr(self, 'user', kwargs.get('user_e', None))
            setattr(self, 'created_at', kwargs.get('created_at', None))
            setattr(self, 'parsed', self.parse_text(kwargs.get('message_e', None)))
            self.list_of_times = self.get_times()
        else:
            self.user = user.id
            self.created_at = message.date
            self.parsed = self.parse_text(message.text)
            self.list_of_times = self.get_times()

    def parse_text(self, message_text):
        #sentences = re.findall("[A-Z].*?[\.!?]", message_text, re.MULTILINE | re.DOTALL)
        se_break = re.compile("""[.!?] \s+  """, re.VERBOSE)
        sentences = se_break.split(message_text)
        print sentences
        return sentences

    def get_times(self):
        m = mp.MessageParser()
        list_of_times = []
        for string in self.parsed:
            list_of_times.append(m.extract_datetime_range(string))

        return list_of_times