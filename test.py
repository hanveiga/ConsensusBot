from data import DataMessage
from datetime import datetime
import bots.meetingsuggestor as ms

def generate_dialog(case='baseline'):
    dialog = []
    if case =='baseline':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do from 6 on Sunday'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': 'I can do at 9 on Sunday'})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': 'I can do at 9 on Sunday. Or on Saturday at 2pm.'})
    elif case=='negation':
        pass
    else:
        pass

    return dialog

def generate_message_stack(dialog):
    list_of_datamessage = []
    for entry in dialog:
        print '%s : %s' %(entry['user_e'], entry['message_e'])
        list_of_datamessage.append(DataMessage(testing=True,**entry))

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

    meeting = meeting_suggestion(times_availability)[0]  # takes highest ranked option
    a, b = meeting
    start, end = a
    text = 'A date could be between %s and %s'%(start.strftime('%H:%M %Y-%m-%d'),end.strftime('%H:%M %Y-%m-%d'))
    print 'Bot response: ' + text

if __name__=='__main__':
    meeting_suggestion = ms.get_suggested_meetings
    simulate_bot_session(meeting_suggestion)

