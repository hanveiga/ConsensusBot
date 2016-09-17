import http.client
import json

conn = http.client.HTTPSConnection("api.tamedia.cloud")
API_KEY = 'd373e302e2f94d699cbb825ee20bfae0'

headers = {
    'accept': "application/json",
    'apikey': API_KEY,
    'content-type': "application/json"
}
def make_poll():
    payload = "{\"type\":\"DATE\",\"title\":\"My Awesome Poll\",\"initiator\":{\"name\":\"Haniball\",\"email\":\"haniball@example.com\"},\"options\":[{\"date\":1462053600000}]}"

    conn.request("POST", "/doodle/v1/polls", payload, headers)

    res = conn.getresponse()
    data = res.read()
    a = json.loads(data)
    print a
    poll_id = a["id"]
    optionsHash = a["optionsHash"]
    adminkey = a["adminKey"]
    return poll_id, optionsHash, adminkey

def add_participants(list_of_users, poll_id,optionHash, adminkey):

    for user in list_of_users:
        #payload = "{\"name\":\""+user+"\"}"
        payload = "{\"name\":\"Haniball S.\"," \
                  "\"preferences\":[0,1,0,2]," \
                  "\"optionsHash\":\""+str(optionHash)+"\"}"

        conn.request("POST", "/doodle/v1/polls/"+str(poll_id)+"/participants?adminKey="+str(adminkey), payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

if __name__=='__main__':
    poll_id, optionHash, adminkey = make_poll()

    add_participants(['john','elisa','brodeo'],poll_id,optionHash,adminkey)

