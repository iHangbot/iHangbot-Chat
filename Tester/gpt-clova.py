import openai
import requests
import sys
import json
from googletrans import Translator
from google.cloud import language_v1
from google.oauth2 import service_account
from collections import Counter
from datetime import datetime
import time
import requests



API_KEY = ''
openai.api_key = API_KEY


sys.stdout.reconfigure(encoding='utf-8')  # 한글 인코딩



# 대화 기록을 저장할 리스트
conversation = [
    {"role": "user", "content": "어린아이말투로 꼭 친절하게 친구처럼 짧게 대화해줘,","date":" "}
]



def call_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")
    return formatted_time




def print_conversation():
    for data in conversation:
        print("role:", data["role"])
        print("content:", data["content"])
        print("date:", data["date"])
        print()
        
while True:
    user_input = input("사용자: ")  # 사용자 입력 받기
    
    if user_input.lower() == "exit":
        break
    if user_input.lower() == "1":
        print_conversation()
        continue
  
    time = call_time()

    # 사용자 입력을 대화 기록에 추가
    conversation.append({"role": "user", "content": user_input, "date": time})
    
    if len(conversation) >=3:
        messages_p = [
            {key: value for key, value in conversation[0].items() if key != "date"},
            {key: value for key, value in conversation[-2].items() if key != "date"},
            {key: value for key, value in conversation[-1].items() if key != "date"}
        ]
    else:
        messages_p = [{key: value for key, value in message.items() if key != "date"} for message in conversation]
        
    print(messages_p)
        

    # GPT에 대화 기록을 전달하여 응답 생성
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages_p
    )

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    

    print("\nGPT: " + response+"\n")  # GPT 응답 출력
    
    
    


