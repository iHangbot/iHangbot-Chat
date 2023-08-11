from pyexpat.errors import messages

import openai
import sys
from datetime import datetime


API_KEY = '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'
openai.api_key = API_KEY

sys.stdout.reconfigure(encoding='utf-8')  # 한글 인코딩

# 대화 기록을 저장할 리스트
messages = [
    {"role": "user", "content": "어린아이말투로 친절하게 친구처럼 대화해주고 답변은 짧게 말해줘."}
]


def call_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")
    return formatted_time


def print_conversation():
    for data in messages:
        print("role:", data["role"])
        print("content:", data["content"])
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
    messages.append({"role": "user", "content": user_input})

    # if len(conversation) >= 3:
    #     messages_p = [
    #         {key: value for key, value in conversation[0].items() if key != "date"},
    #         {key: value for key, value in conversation[-2].items() if key != "date"},
    #         {key: value for key, value in conversation[-1].items() if key != "date"}
    #     ]
    # else:
    #     messages_p = [{key: value for key, value in message.items() if key != "date"} for message in conversation]
    #
    # print(messages_p)

    # GPT에 대화 기록을 전달하여 응답 생성
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages, #여기가 문제였네
        temperature=0.15,
        frequency_penalty=2.0,
    )
    print(messages)

    #gpt 대화내용을 기억해주자
    gpt_converstation = completion.choices[0].message["content"].strip()

    messages.append(({"role": "assistant", "content": gpt_converstation}))



    print("\nGPT: " + gpt_converstation + "\n")  # GPT 응답 출력
