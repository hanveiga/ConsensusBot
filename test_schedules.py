from data import DataMessage
from datetime import datetime
import bots.meetingsuggestor as ms
import parsing.MessageParser as mp
from collections import defaultdict
import doodle.export_doodle as doodle

m = mp.MessageParser()


HOUR_FORMAT = '%H:%M'
DATA_FORMAT = '%d/%m'

DATE_FORMAT = '%H:%M %d/%m'

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

    elif case == 'chatter':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do from 6 on Sunday.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do from 9 on Sunday. My dog is sick so I can't on Saturday."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "Sorry about your dog."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I won't be able to come on Sunday."})

    elif case == 'buddies':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do between 8pm and 12pm.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do in 45 minutes"})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "Had the most awful day."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I can do at half past four."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I can do tomorrow at half past four."})

    elif case == 'moredays':
        dialog.append({'user_e': 'John',
                       'created_at': datetime.now(),
                       'message_e': 'I can do Monday.'})
        dialog.append({'user_e': 'Mark',
                       'created_at': datetime.now(),
                       'message_e': "I can do Monday."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "Had the most awful day."})
        dialog.append({'user_e': 'Jane',
                       'created_at': datetime.now(),
                       'message_e': "I can do Monday."})
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
    export(message_stack)
    get_consensus(message_stack,meeting_suggestion)


def export(message_stack):
    """Adds data entities proposed by user

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    all_users = []
    for user in message_stack:
        if user.user in all_users:
            pass
        else:
            all_users.append(user.user)

    all_options_text = []
    preferences = defaultdict(list)
    meeting_length = 2
    full_preferences = defaultdict(list)
    if message_stack == []:
        return #bot.sendMessage(update.message.chat_id, text='There are no entries to export.')
    else:
        new_consensus = meeting_suggestion(message_stack, meeting_length)
        for result in new_consensus:
            print result.date_from
            print result.date_to
            print result.users_to_ask
            all_options_text.append({'text':result.date_from.strftime(DATE_FORMAT)+'-'+result.date_to.strftime(DATE_FORMAT)})
            for user in all_users:
                if user in result.users_to_ask:
                    full_preferences[user].append(0)# negative
                else:
                    full_preferences[user].append(1)
                # positive

    print full_preferences
    #list_options=[]
    #for key in all_options.keys():
    #    list_options.append({"text":key})
    #print full_preferences
    doodle.generate_doodle(full_preferences,all_options_text)
    # call doodle functions

def get_consensus(message_stack, meeting_suggestion):
    meeting_length = 2
    new_consensus = meeting_suggestion(message_stack, meeting_length)

    start = new_consensus[0].date_from
    end = new_consensus[0].date_to
    users = new_consensus[0].users_to_ask
    if users == []:
        print "We have a consensus"
        print 'A date could be between {} and {}'.format(start.strftime(DATA_FORMAT), end.strftime(DATA_FORMAT))

    else:
        reply_keyboard = [['Yes', 'No']]

        for user in users:
            schedule_text = "@"+user
            schedule_text = schedule_text + ' Can you make it between {} and {} on {}'.format(start.strftime(HOUR_FORMAT),
                                                              end.strftime(HOUR_FORMAT),
                                                                 start.strftime(DATA_FORMAT))
            print schedule_text


if __name__=='__main__':
    meeting_suggestion = ms.get_suggested_meetings_topology_sort
    simulate_bot_session(meeting_suggestion, case='chatter')

