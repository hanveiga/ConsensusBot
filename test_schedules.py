from data import DataMessage
from datetime import datetime
import bots.meetingsuggestor as ms

DATA_FORMAT = '%H:%M %Y-%m-%d'

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
    else:
        pass

    return dialog

def generate_message_stack(dialog):
    list_of_datamessage = []
    for entry in dialog:
        print '%s : %s' %(entry['user_e'], entry['message_e'])
        mes = DataMessage(testing=True,**entry)
        print mes.list_of_times
        list_of_datamessage.append(mes)

    return list_of_datamessage

def simulate_bot_session(meeting_suggestion, case='baseline'):
    dialog = generate_dialog(case)

    message_stack = generate_message_stack(dialog)

    get_consensus(message_stack,meeting_suggestion)


def get_consensus(message_stack, meeting_suggestion):
    meeting_length = 2
    new_consensus = meeting_suggestion(message_stack, meeting_length)
    _, start, end, users = new_consensus[0]

    if users == []:
        print "We have a consensus"
        print 'A date could be between {} and {}'.format(start.strftime(DATA_FORMAT), end.strftime(DATA_FORMAT))

    else:
        reply_keyboard = [['Yes', 'No']]

        for user in users:
            schedule_text = "@"+user
            schedule_text = schedule_text + ' Can you make it between {} and {}'.format(start.strftime(DATA_FORMAT),
                                                                                        end.strftime(DATA_FORMAT),)
            print schedule_text


if __name__=='__main__':
    meeting_suggestion = ms.get_suggested_meetings_topology_sort
    simulate_bot_session(meeting_suggestion, case='baseline')

