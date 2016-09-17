from data import DataMessage
from datetime import datetime
import bots.meetingsuggestor as ms
import parsing.MessageParser as mp

m = mp.MessageParser()

def generate_dialog(case='baseline'):
    dialog = []
    if case =='baseline':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do from 6 on Sunday.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do at 9 on Sunday."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': 'I can do at 9 on Sunday. Or on Saturday at 2pm.'})
    elif case=='negation':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do from 6 on Sunday.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do at 9 on Sunday. I can not do 9 on Monday."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I can do at 9 on Sunday. Or on Saturday at 2pm."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I will not be able to come on Friday"})
    elif case=='chatter':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do from 6 on Sunday.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do at 9 on Sunday. My dog is sick so I can't on Saturday."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "Sorry about your dog."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I won't be able to come on Friday, but Sunday works for me."})
    else:
        pass

    return dialog

def generate_message_stack(dialog):
    list_of_datamessage = []
    for entry in dialog:
        print '%s : %s' %(entry['user_e'], entry['message_e'])
        if m.extract_intent(entry['message_e']) == 'times':
            mes = DataMessage(testing=True,**entry)
            print mes.list_of_times
            list_of_datamessage.append(mes)

    return list_of_datamessage

def simulate_bot_session(meeting_suggestion, case='baseline'):
    dialog = generate_dialog(case)

    message_stack = generate_message_stack(dialog)

    get_consensus(message_stack,meeting_suggestion)


def get_consensus(message_stack, meeting_suggestion):
    times_availability = []
    for message in message_stack:
        for interval in message.list_of_times:
            times_availability.append(interval)
    window_size = 2
    meeting = meeting_suggestion(message_stack,window_size)[0]  # takes highest ranked option
    print meeting
    a, start, end, c = meeting
    text = 'A date could be between %s and %s'%(start.strftime('%H:%M %Y-%m-%d'),end.strftime('%H:%M %Y-%m-%d'))
    print 'Bot response: ' + text

if __name__=='__main__':
    meeting_suggestion = ms.get_suggested_meetings_topology_sort
    simulate_bot_session(meeting_suggestion, case='chatter')

