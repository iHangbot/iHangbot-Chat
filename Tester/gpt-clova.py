import openai
import requests
import sys
import json
import websockets
from googletrans import Translator
from google.cloud import language_v1
from google.oauth2 import service_account
from collections import Counter
from datetime import datetime
import time
import requests



API_KEY = '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'
openai.api_key = API_KEY


sys.stdout.reconfigure(encoding='utf-8')  # 한글 인코딩



# 대화 기록을 저장할 리스트
conversation = [
    {"role": "user", "content": "어린아이말투로 친절하게 꼭 반말로 대화해줘,","date":" "}
]

# 감정 분석을 저장할 리스트
analyze_data =[
    {"content":"" ,"negative":"" ,"positive":"" ,"neutral":"" ,"date":" "}
]

key_word =[
    {"keyword":"" , "count":"","date":""}
]

Category =[
    {"category":"" , "confidence":"" , "date":""}
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
        
        

def print_analyze_data():
    for data in analyze_data:
        print("Content:", data["content"])
        print("negative:", data["negative"])
        print("positive:", data["positive"])
        print("neutral:", data["neutral"])
        print("date:", data["date"])
        print()
        
        
        
def print_key_word():
    for item in key_word:
        keyword = item["keyword"]
        count = item["count"]
        date = item["date"]
        print(f"Keyword: {keyword}, count: {count}, Date : {date}")


def print_category():
    for item in Category:
        category = item["category"]
        confidence = item["confidence"]
        date = item["date"]
        print(f"Category: {category}, Confidence: {confidence}, date : {date}")



def sentiment_store(content,jsonD):
    time = call_time()
    negative_value = jsonD["document"]["confidence"]["negative"]
    positive_value = jsonD["document"]["confidence"]["positive"]
    neutral_value = jsonD["document"]["confidence"]["neutral"]
    analyze_data.append({"content":content,"negative":negative_value,"positive":positive_value,"neutral":neutral_value,"date":time})



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
        time = call_time()
        sentiment_store(content,jsonD)
        
        return jsonD
    else:
        print("Error: " + response.text)
        
        
        
        
def extract_keywords(text):
    key_path = 'C:/Users/yechan/gpt-3/service_account_key.json'
    time = call_time()

    # 서비스 계정 키를 사용하여 Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={'document': document})

    entity_names = [entity.name for entity in response.entities]
    top_keywords = Counter(entity_names).most_common(5)

    for keyword, count in top_keywords:
        key_word.append({"keyword":keyword , "count":count, "date":time})
        
        
        
            
        
        
        
        
def translate_text(text, source_language, target_language):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text



def classify_document(text):
    key_path = 'C:/Users/yechan/gpt-3/service_account_key.json'
    time = call_time()

    # 한국어 문장을 영어로 번역
    translated_text = translate_text(text, 'ko', 'en')

    # 서비스 계정 키를 사용하여 Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=translated_text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.classify_text(request={'document': document})

    categories = response.categories

    if categories:
        for category in categories:
            print(f'category: {category.name}, confidence: {category.confidence}')
            Category.append({"category":category.name , "confidence":category.confidence, "date":time})
    else:
        print('No categories found.')






while True:
    user_input = input("사용자: ")  # 사용자 입력 받기
    
    if user_input.lower() == "exit":
        break
    if user_input.lower() == "1":
        print_conversation()
        continue
    
    if user_input.lower() == "2":
        print_analyze_data()    
        
        url='http://192.168.0.177:8080/sentiment/getData'
        json_data = json.dumps(analyze_data[1:])
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(json_data)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        continue
    
    if user_input.lower() == "3":
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = "\n".join(content_list)
        extract_keywords(merged_content)
        
        url='http://192.168.0.177:8080/keyword/getKeyWord'
        json_data = json.dumps(key_word[2:])
        print(json_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(response)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        continue
    
    if user_input.lower() == "4":
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = " ".join(content_list)
        classify_document(merged_content)  
        
        url='http://192.168.0.177:8080/keyword/getConcern'
        json_data = json.dumps(Category[1:])
        print(json_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(response)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
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

    
    jsonD=analyze_sentiment(user_input)
    

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    

    print("\nGPT: " + response+"\n")  # GPT 응답 출력
    
    
    


