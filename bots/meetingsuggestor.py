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


