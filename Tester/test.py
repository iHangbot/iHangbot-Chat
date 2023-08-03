import requests

# 서버 URL
server_url = 'http://localhost:8079/api/chat'

while True:
    # 사용자로부터 메시지 입력 받기
    message = input()
    
    if message == 'exit':
        break

    # POST 요청 보내기
    response = requests.post(server_url, json={'string': message})

    # 응답 결과 확인
    if response.status_code == 200:
        data = response.json()
        print('서버 응답:', data)
    else:
        print('요청 실패:', response.status_code)
