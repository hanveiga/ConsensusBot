import requests
import http.client
import json
from settigns import API_KEY

#conn = http.client.HTTPSConnection("api.tamedia.cloud")

headers = {
    'accept': "application/json",
    'apikey': API_KEY,
    'content-type': "application/json"
}

print(API_KEY)

def _create_poll(choices_names):
    sent_data = {
        'title': 'Consensus Bot result',
        'initiator': {
            'name': 'Pawel Kaminski',
            'email': 'pawelkaminski@mailinator.com'
        },
        'type': 'TEXT',
        'options': choices_names,
    }
    print(sent_data)
    returned_request = requests.post('https://api.tamedia.cloud/doodle/v1/polls', json=sent_data, headers=headers)
    json_req = returned_request.json()
    print json_req
    return json_req['id'], json_req['optionsHash']


def _add_participants(user_preferences, user, poll_id, options_hash):
    sent_data = {
        'name': user,
        'preferences': user_preferences,
        'optionsHash': options_hash,
    }
    print(sent_data)
    requests.post('https://api.tamedia.cloud/doodle/v1/polls/{}/participants'.format(poll_id), json=sent_data,
                  headers=headers)


def generate_doodle(user_preferences, choices_intervals):
    poll_id, options_hash = _create_poll(choices_intervals)
    print(poll_id)
    for user, preferences in user_preferences.items():
        _add_participants(preferences, user, poll_id, options_hash)

    return 'http://doodle.com/poll/'+str(poll_id)

#import datetime
#generate_doodle({'Andrzej': [0,], 'Marysia': [1,]}, [{'start': datetime.datetime.now().isoformat(),
#                                                     'end': datetime.datetime.now().isoformat()}, ])
