import requests, json
data = open('dream-network16.ttl').read()
headers = {'Content-Type': 'text/turtle;charset=utf-8'}
r = requests.post('http://localhost:3030/ds/data?default', data=json.dumps(data, ensure_ascii=False).encode('utf-8')), headers=headers)