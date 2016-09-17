import heapq
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

MAX_SCORE_USER_PLUS = 2.0
MAX_SCORE_USER_MINUS = -2.0


def _get_scores(timestamps_list, score_modifier, right_window, left_window, window_size):
    score = 0.0
    for entity in timestamps_list:
        if entity[0] > right_window:
            return score
        if entity[1] < left_window:
            continue
        if entity[1] > right_window and entity[0] < left_window:
            score += score_modifier
        elif entity[1] > right_window and entity[0] >= left_window:
            time_diff = right_window - entity[0]
            score += score_modifier*(time_diff.seconds/float(window_size*60*60))
        elif entity[1] > left_window and entity[0] <= left_window:
            time_diff = entity[1] - left_window
            score += score_modifier*(time_diff.seconds/float(window_size*60*60))
        elif entity[1] > left_window and entity[0] > left_window:
            time_diff = entity[1] - entity[0]
            score += score_modifier*(time_diff.seconds/float(window_size*60*60))
    return score


def get_suggested_meetings_topology_sort(list_of_data, window_size):
    split_by_users = {}
    for element in list_of_data:
        if element.user not in split_by_users:
            # from /to /creation/ valuation
            split_by_users[element.user] = []
        for date_from, date_to, flag_av in element.list_of_times:
            split_by_users[element.user].append((date_from, date_to, element.created_at, (not flag_av),))

    min_bound = None
    max_bound = None
    ordered_by_users = {}
    for user, values in split_by_users.items():
        ordered_by_users[user] = sorted(values)
        # hack less code
        min_bound = ordered_by_users[user][0][0]
        max_bound = ordered_by_users[user][0][1]

    for _, values in split_by_users.items():
        for val in values:
            min_bound = min(val[0], min_bound)
            max_bound = max(val[1], max_bound)

    min_bound -= timedelta(hours=window_size)
    max_bound += timedelta(hours=window_size)
    # right now only true valuation
    joined_plus_by_users = {}
    joined_minus_by_users = {}

    for user, times in ordered_by_users.items():
        returned_list_plus = []
        returned_list_minus = []
        lower_bound = None
        current_upper_bound = None
        current_flag = None
        current_adding_time = None
        for time_tup in times:
            if not lower_bound:
                lower_bound, current_upper_bound, current_adding_time, current_flag = time_tup
            elif current_upper_bound >= time_tup[0]:

                if time_tup[3] == current_flag:
                    current_upper_bound = max(time_tup[1], current_upper_bound)
                else:
                    if current_adding_time > time_tup[2]:
                        continue
                    # where override can happen not the exact algorithm!
                    current_upper_bound = time_tup[1]
                    if lower_bound < current_upper_bound:
                        if current_flag:
                            returned_list_plus.append((lower_bound, current_upper_bound,))
                        else:
                            returned_list_minus.append((lower_bound, current_upper_bound,))
                    lower_bound, current_upper_bound, current_adding_time, current_flag = time_tup

            else:
                if current_flag:
                    returned_list_plus.append((lower_bound, current_upper_bound,))
                else:
                    returned_list_minus.append((lower_bound, current_upper_bound,))
                lower_bound, current_upper_bound, current_adding_time, current_flag = time_tup

        if current_flag:
            returned_list_plus.append((lower_bound, current_upper_bound,))
        else:
            returned_list_minus.append((lower_bound, current_upper_bound,))
        joined_plus_by_users[user] = returned_list_plus
        joined_minus_by_users[user] = returned_list_minus

    left_window = min_bound
    right_window = left_window + timedelta(hours=window_size)
    # arbitrary number
    # score, from, to, bad users
    result_heap = []
    users_list = ordered_by_users.keys()

    # algorithm with negations
    while right_window <= max_bound:
        # don t care about complexity
        users_to_ask = []
        total_score = 0
        for user in users_list:
            score = 0

            score += _get_scores(joined_plus_by_users.get(user, []), MAX_SCORE_USER_PLUS, right_window,
                                 left_window, window_size)

            score += _get_scores(joined_minus_by_users.get(user, []), MAX_SCORE_USER_MINUS, right_window,
                                 left_window, window_size)
            if score != 2:
                users_to_ask.append(user)
            total_score += score

        heapq.heappush(result_heap, (total_score, left_window, right_window, users_to_ask,))
        right_window += timedelta(hours=1)
        left_window += timedelta(hours=1)

    return heapq.nlargest(5, result_heap)
