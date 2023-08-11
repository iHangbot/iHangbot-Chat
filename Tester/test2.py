import requests
import json

url = 'http://localhost:8079/api/chat/test122'
headers = {'Content-Type': 'application/json'}

while (True):
    prompt = input("질문을 입력하세요: ")
    data = {"string" : prompt}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.json())