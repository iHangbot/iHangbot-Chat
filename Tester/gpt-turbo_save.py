import openai
import sys

API_KEY = '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'
openai.api_key = API_KEY

sys.stdout.reconfigure(encoding='utf-8')  # 한글 인코딩

# 대화 기록을 저장할 리스트
conversation = [
    {"role": "system", "content": "어린아이 말투로 반말로 친근하게 대화해줘"}
]

while True:
    user_input = input("사용자: ")  # 사용자 입력 받기
    
    if user_input.lower() == "exit":
        break

    # 사용자 입력을 대화 기록에 추가
    conversation.append({"role": "user", "content": user_input})

    # GPT에 대화 기록을 전달하여 응답 생성
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": response})

    print("\nGPT: " + response+"\n")  # GPT 응답 출력