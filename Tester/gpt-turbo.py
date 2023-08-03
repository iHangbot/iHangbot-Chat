import openai
import requests
import sys
import json
from flask import Flask, jsonify,request

API_KEY = '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'
openai.api_key = API_KEY


sys.stdout.reconfigure(encoding='utf-8')  # 한글 인코딩



# 대화 기록을 저장할 리스트
conversation = [
    {"role": "system", "content": "어린아이말투로 친근하게 대화해줘"}
]
# 감정 분석을 저장할 리스트
analyze_data =[
    {"content":"" ,"Negative":"","Positive":"","Neutral":""}
]

def print_analyze_data():
    for data in analyze_data:
        print("Content:", data["content"])
        print("Negative:", data["Negative"])
        print("Positive:", data["Positive"])
        print("Neutral:", data["Neutral"])
        print()
        
        
def print_conversation():
    for data in conversation:
        print("role:", data["role"])
        print("content:", data["content"])
        print()



def sentiment_store(content,jsonD):
    negative_value = jsonD["document"]["confidence"]["negative"]
    positive_value = jsonD["document"]["confidence"]["positive"]
    neutral_value = jsonD["document"]["confidence"]["neutral"]
    
    analyze_data.append({"content":content,"Negative":negative_value,"Positive":positive_value,"Neutral":neutral_value})





def analyze_sentiment(content):
    client_id = "y31l8r0q5p"
    client_secret = "6VBpXzn7aDXU1jgLRGobWFnl85C3CP7sIPKrdPQH"
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        "content": content
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code
    if rescode == 200:
        jsonD = response.json()
        sentiment_store(content,jsonD)
        
        return jsonD
    else:
        print("Error: " + response.text)






app = Flask(__name__)


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # 사용자 입력 받기
    print("채팅이 들어옴.")
    
    if user_input.lower() == "exit":
        exit
    if user_input.lower() == "1":
        print_conversation()
    if user_input.lower() == "2":
        print_analyze_data()    
        

    # 사용자 입력을 대화 기록에 추가
    conversation.append({"role": "user", "content": user_input})

    # GPT에 대화 기록을 전달하여 응답 생성
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    
    jsonD=analyze_sentiment(user_input)
    

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": response})
    

    print("\nGPT: " + response+"\n")  # GPT 응답 출력
    return jsonify(response)



if __name__ == '__main__':
    from waitress import serve
    print("server stating....")
    serve(app, host='0.0.0.0', port=8000)
    
    
    


