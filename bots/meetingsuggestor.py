from datetime import timedelta
def get_suggested_meetings(intervals):
    events = sorted([x[0] for x in intervals]+[x[1] for x in intervals])
    meetings = dict()
    for i in range(len(events)-1):
        rangefrom = events[i]
        rangeto = events[i+1]
        c = 0
        for interval in intervals:
            if interval[0] <= rangefrom and interval[1] >= rangeto:
                c+=1
        meetings[(rangefrom,rangeto)] = c
    meetings = sorted(meetings.items(),key= lambda x: x[1], reverse= True)
    return meetings


'''
from parsing.MessageParser import MessageParser

m = MessageParser()
interval1 = m.extract_datetime_range('lets meet next friday')
interval2 = m.extract_datetime_range('lets meet next week')
interval3 = m.extract_datetime_range('how about 5 pm next friday ?')
for meeting in get_suggested_meetings([interval1, interval2, interval3]):
    print meeting
'''

MAX_SCORE_USER_PLUS = 2
MAX_SCORE_USER_MINUS = -2


def _get_scores(timestamps_list, score_modifier, right_window, left_window, window_size):
    score = 0
    for entity in timestamps_list:
        if entity[0] > right_window:
            return score
        if entity[1] < left_window:
            continue
        if entity[1] > right_window and entity[0] < left_window:
            score += score_modifier
        elif entity[1] > right_window and entity[0] >= left_window:
            time_diff = entity[0] - right_window
            score += score_modifier*(time_diff.seconds/(window_size*60*60))
        elif entity[1] > left_window and entity[0] <= left_window:
            time_diff = left_window - entity[1]
            score += score_modifier*(time_diff.seconds/(window_size*60*60))
        elif entity[1] > left_window and entity[0] > left_window:
            time_diff =entity[0] - entity[1]
            score += score_modifier*(time_diff.seconds/(window_size*60*60))
    return score


def get_suggested_meetings_topology_sort(list_of_data, window_size):
    split_by_users = {}
    for element in list_of_data:
        if not split_by_users[element.user]:
            # from /to /creation/ valuation
            split_by_users[element.user] = []
        for date_from, date_to in element.list_of_times:
            split_by_users[element.user].append((date_from, date_to, element.created_at, True,))

    min_bound = None
    max_bound = None
    ordered_by_users = {}
    for user, values in split_by_users.items():
        ordered_by_users[user] = sorted(values)
        # hack less code
        min_bound = ordered_by_users[user][0]
        max_bound = ordered_by_users[user][1]

    for values in split_by_users:
        for val in values:
            min_bound = min(val[0], min_bound)
            max_bound = max(val[1], max_bound)

    # right now only true valuation
    joined_plus_by_users = {}
    joined_minus_by_users = {}
    #TODO add them

    # TODO(scezar): add minus and care of time override!
    for user, times in ordered_by_users.items():
        returned_list = []
        lower_bound = None
        current_upper_bound = None
        for t in times:
            if not lower_bound:
                lower_bound = t[0]
                current_upper_bound = t[1]
            elif current_upper_bound >= t[0]:
                current_upper_bound = t[1]
            else:
                returned_list.append((lower_bound, current_upper_bound,))
                lower_bound = t[0]
                current_upper_bound = t[1]

        returned_list.append((lower_bound, current_upper_bound,))
        joined_plus_by_users[user] = returned_list

    left_window = min_bound
    right_window = left_window + timedelta(hours=window_size)
    # arbitrary number
    # from, to, score, bad users
    best_score = (None, None, -1000, [])
    users_list = ordered_by_users.keys()
    # algorithm with negations
    while right_window > max_bound:
        # don t care about complexity
        users_to_ask = []
        total_score = 0
        for user in users_list:
            score = 0

            score += _get_scores(joined_plus_by_users.get(user, []), MAX_SCORE_USER_PLUS, right_window,
                                 left_window, window_size)

            score += _get_scores(joined_plus_by_users.get(user, []), MAX_SCORE_USER_MINUS, right_window,
                                 left_window, window_size)
            if score != 2:
                users_to_ask.append(user)
            total_score += score

        if total_score > best_score[2]:
            best_score = (left_window, right_window, total_score, users_to_ask)
        right_window += timedelta(hours=1)
        left_window += timedelta(hours=1)
