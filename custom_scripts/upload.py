import requests, json
data = open('dream-network16.ttl').read()
formattedData = json.dumps(data, ensure_ascii=False).encode('utf-8')
headers = {'Content-Type': 'text/turtle;charset=utf-8'}
r = requests.post('http://localhost:3030/ds/data?default', data=formattedData, headers=headers)

data = open('dream-network16.nt', "r", encoding="utf-8").read()
formattedData = json.dumps(data)
headers = {'Content-Type': 'application/n-triples'}
r = requests.post('http://localhost:3030/ds/data?default', data=formattedData, headers=headers)



application/n-triples