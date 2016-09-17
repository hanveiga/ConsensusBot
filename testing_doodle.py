import http.client

conn = http.client.HTTPSConnection("api.tamedia.cloud")

payload = "{\"name\":\"Bro S.\",\"preferences\":[0,1,0,2],\"optionsHash\":\"b38b35466fc5979443518dd1261cb2df\"}"

headers = {
    'accept': "application/json",
    'apikey': "a2e2b89b30774fe98f6d60bcc9e11ca9",
    'content-type': "application/json"
    }

conn.request("POST", "/doodle/v1/polls/gdhugaxw2hsku4v3/participants?adminKey=32ca44xd", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
