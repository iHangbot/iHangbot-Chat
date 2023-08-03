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
from flask import Flask, request,jsonify
from multiprocessing import Process
from konlpy.tag import Okt
import numpy as np
import threading
import time


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



def sentiment_store(content,average_negative,average_positive,average_neutral):
    time = call_time()
    negative_value = average_negative
    positive_value = average_positive
    neutral_value = average_neutral
    analyze_data.append({"content":content,"negative":negative_value,"positive":positive_value,"neutral":neutral_value,"date":time})




def analyze_sentiment(content):
    
    okt = Okt()
    CheckSentence = False

    # 품사 태깅
    tagged = okt.pos(content)
    print(tagged)

    # 태그가 'Adjective' , 'Noun'+'Josa'+'Verb' , 'Noun'+'Verb'인 단어들만 추출
    adjectives = []
    for i in range(len(tagged)) :
        word, tag = tagged[i]
        
        if tag == 'Adjective':
            adjectives.append(word)
            CheckSentence = True
            
        elif tag == 'Verb' and i > 0 and (tagged[i-1][1] in ('Josa') and tagged[i-2][1] in ['Noun']) :
            if(i < len(tagged)-1 and (tagged[i+1][1] in ('Verb'))) :
                adjectives.append(tagged[i-2][0]+tagged[i-1][0] + word +tagged[i+1][0])
                CheckSentence = True
            else :
                adjectives.append(tagged[i-2][0]+tagged[i-1][0] + word)
                CheckSentence = True
                
        elif tag == 'Verb' and i > 0 and (tagged[i-1][1] in ('Noun')) :
            if(i < len(tagged)-1 and (tagged[i+1][1] in ('Verb'))) :
                adjectives.append(tagged[i-1][0] + word + tagged[i+1][0])
                CheckSentence = True
            else :
                adjectives.append(tagged[i-1][0] + word)
                CheckSentence = True
        elif tag =='Verb' and i > 0 :
            adjectives.append(word)
            CheckSentence = True
    print(adjectives)
    count = len(adjectives)
    print(count)





    if(CheckSentence == True):
        client_id = "y31l8r0q5p"
        client_secret = "6VBpXzn7aDXU1jgLRGobWFnl85C3CP7sIPKrdPQH"
        url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"
        }
        
        negative_scores = []
        positive_scores = []
        neutral_scores = []

        negative_scores_p = []
        positive_scores_p = []
        neutral_scores_p = []


        for verb in adjectives:
            data = {
                "content": verb
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)
            rescode = response.status_code
            if rescode == 200:
                jsonD = response.json()
                print(f"감정 분석 결과 for '{verb}': ", jsonD)
                if((jsonD['document']['confidence']['neutral']) < 0.30) :
                    negative_scores.append(jsonD['document']['confidence']['negative'])
                    positive_scores.append(jsonD['document']['confidence']['positive'])
                    neutral_scores.append(jsonD['document']['confidence']['neutral'])
                else :
                    negative_scores_p.append(jsonD['document']['confidence']['negative'])
                    positive_scores_p.append(jsonD['document']['confidence']['positive'])
                    neutral_scores_p.append(jsonD['document']['confidence']['neutral'])
                print()
            else:
                print("Error: " + response.text)
                
        if(len(negative_scores) != 0 ):        
            average_negative = np.mean(negative_scores)
            average_positive = np.mean(positive_scores)
            average_neutral = np.mean(neutral_scores)
        else :
            average_negative = np.mean(negative_scores_p)
            average_positive = np.mean(positive_scores_p)
            average_neutral = np.mean(neutral_scores_p)

        print(f"Negative scores average: {average_negative}")
        print(f"Positive scores average: {average_positive}")
        print(f"Neutral scores average: {average_neutral}")

        print()





    else :
        client_id =  "y31l8r0q5p"
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
            average_negative = (jsonD['document']['confidence']['negative'])
            average_positive = (jsonD['document']['confidence']['positive'])
            average_neutral = (jsonD['document']['confidence']['neutral'])
            print(jsonD)
        else:
            print("Error: " + response.text)
                
    sentiment_store(content,average_negative,average_positive,average_neutral)
            
    
        
        
        
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
            name = translate_text(category.name,'en','ko')
            print(f'category: {name}, confidence: {category.confidence}')
            Category.append({"category":name , "confidence":category.confidence})
    else:
        print('No categories found.')






def thread1(): # 스레드1
    while True:
        time.sleep(20) # 일단 지금 60초로 설정함 추 후에 바꿔야함.!
        print_conversation
        print_analyze_data
        print_category
        print_conversation
        
        
        #감정 분석 결과 전송
        url='http://52.79.225.144:8080/sentiment/getData' # URL 변경 해줘야해요.......
        json_data = json.dumps(analyze_data[1:])
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(json_data)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력




        #키워드 분석 결과 전송
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = "\n".join(content_list)
        extract_keywords(merged_content)
        print_key_word()
        
        url='http://52.79.225.144:8080/keyword/getKeyWord'
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
            
            
            
            
            
        #주제 분석 결과 전송
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = " ".join(content_list)
        try:
            classify_document(merged_content)
            print_category()
        except Exception as e:
            print("오류 내용 : ", str(e))
        #print_category()    
        
        url='http://52.79.225.144:8080/keyword/getConcern'
        json_data = json.dumps(Category[1:])
        print(json_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(response) # 서버로 부터 응답(response) 받았을 때;;;
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        
        
thread = threading.Thread(target=thread1)
thread.start()


app = Flask(__name__)

@app.route('/postSuggestion', methods=['POST'])#POST변경해야함
def repost():
    print(request.get_json())
    data = request.get_json()
    keyword = data
    print(keyword)
    report=""
    for data in keyword:
        joindata = data['keyword']
        joindata += ","
        report += joindata
    report = report[:-1]
    report += "들이 아이의 관심사인데 이를 기반으로 부모님께 제안글을 두 문장 이내로 작성해줘"
    print(report)
    
    messages_p = [
    {"role": "system", "content": report},
    ]
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages_p,
    temperature=0,
    presence_penalty=0.7,
    frequency_penalty=1.0
    )
    
    #url='http://10.11.101.49:8080/keyword/suggestion'
    response = completion['choices'][0]['message']['content']
    print(response)
    
    json_data = json.dumps(response)
    #print(response)
    
    #headers = {'Content-Type': 'application/json'}
    #response2 = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
    #print(response2)      
    #if response2.status_code == 200:  # 요청이 성공했을 경우
    #    print('데이터 전송 성공')
    #else:
    #    print('데이터 전송 실패:', response2.status_code)  # 요청 실패 시 상태 코드 출력
    #    print('오류 내용:', response2.text)  # 오류 내용 출력
    #print(response) 
    
    return jsonify({'message': response}), 200
    
    

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('string')  # 사용자 입력 받기
    print("수신 완료")
   
    if str(user_input).lower() == "1":  
        print_conversation()
        return jsonify(), 200
    if str(user_input).lower() == "2":
        print_analyze_data()    
        
        url='http://52.79.225.144:8080/sentiment/getData'
        json_data = json.dumps(analyze_data[1:])
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(json_data)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        return jsonify({'message': response}), 204
            
    if str(user_input).lower() == "3":
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = "\n".join(content_list)
        extract_keywords(merged_content)
        print_key_word()
        
        url='http://52.79.225.144:8080/keyword/getKeyWord'
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
        return jsonify({'message': response}), 204
            
    if str(user_input).lower() == "4":
        content_list = [data["content"] for data in conversation[1:]]
        merged_content = " ".join(content_list)
        try:
            classify_document(merged_content)
            print_category()
        except Exception as e:
            print("오류 내용 : ", str(e))
        #print_category()    
        
        url='http://52.79.225.144:8080/keyword/getConcern'
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
        return jsonify({'message': response}), 204





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

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages_p,
    temperature=0,
    frequency_penalty=2.0
    )

    
    analyze_sentiment(user_input)
    

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    

    print("\nGPT: " + response+"\n")  # GPT 응답 출력
    
    return jsonify({'message': response}), 200

if __name__ == '__main__':
    from waitress import serve
    print("server stating....")
    serve(app, host='0.0.0.0', port=8079)
    
    


