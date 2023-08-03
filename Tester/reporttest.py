import json
import requests

# 주어진 JSON 데이터
json_data = '''
{
  "status": 200,
  "message": "성공",
  "data": {
    "keywords": [
      {
        "keyword": "유치원",
        "count": 9
      },
      {
        "keyword": "친구",
        "count": 6
      },
      {
        "keyword": "왕따",
        "count": 3
      },
      {
        "keyword": "우울",
        "count": 3
      },
      {
        "keyword": "전학",
        "count": 3
      }
    ],
    "concerns": [
      "/Books & Literature/Literary Classics",
      "/Arts & Entertainment"
    ]
  }
}
'''

# JSON 데이터를 파싱하여 딕셔너리로 변환
data = json.loads(json_data)

# POST 요청을 보낼 URL
url = 'http://localhost:8079/keyword/report'

# POST 요청 보내기
response = requests.post(url, json=data)

# 응답 결과 확인
if response.status_code == 200:
    data = response.json()
    print('서버 응답:', data)
else:
    print('요청 실패:', response.status_code)

