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
from flask import Flask,request,jsonify
from multiprocessing import Process
from konlpy.tag import Okt
import numpy as np
import threading
import time
import schedule

import Analyze
import Config
import Data
import Utils


def job():
    
        Utils.print_conversation
        Utils.print_analyze_data
        Utils.print_category
        Utils.print_conversation
        time = Utils.call_time()
    
        for id in Data.IdArray:


            #키워드 분석 결과 전송
            content_list = [data["content"] for data in Data.conversation[1:] if data["role"] == "user" and data['username'] == id and data['time'] == time]
            merged_content = "\n".join(content_list)
            Analyze.extract_keywords(merged_content,id)
            Utils.print_key_word()
            
            url='http://52.79.225.144:8080/keyword/getKeyWord'
            filtered_data = [item for item in Data.key_word if item.get("username") == id]
            json_data = json.dumps(filtered_data)
            print(json_data)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
            print(response)       
            if response.status_code == 200:  # 요청이 성공했을 경우
                print('데이터 전송 성공')
            else:
                print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
                print('오류 내용:', response.text)  # 오류 내용 출력
                
                
                
                
            content_list = [data["content"] for data in Data.conversation[1:] if data["role"] == "user" and data['username'] == id and data['time'] == time]
            merged_content = "\n".join(content_list)    
            #주제 분석 결과 전송
            try:
                Analyze.classify_document(merged_content,id)
                Utils.print_category()
            except Exception as e:
                print("오류 내용 : ", str(e))
            #print_category()    
            
            url='http://52.79.225.144:8080/keyword/getConcern'
            filtered_data = [item for item in Data.Category if item.get("username") == id]
            json_data = json.dumps(filtered_data)
            print(json_data)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
            print(response)
            if response.status_code == 200:  # 요청이 성공했을 경우
                print('데이터 전송 성공')
            else:
                print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
                print('오류 내용:', response.text)  # 오류 내용 출력
            Data.key_word.clear()
            Data.Category.clear()
            




schedule.every().day.at("23:50").do(job)



def thread1(): # 스레드1
    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
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
    {"role": "user", "content": report},
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
    
    

@app.route('/api/chat/<id>', methods=['POST'])
def chat(id):
    time = Utils.call_time()
    data = request.json
    user_input = data.get('string')  # 사용자 입력 받기
    Data.Add_Id(id)
    Data.list_all_ids()
    
    print("수신 완료")
   
    if str(user_input).lower() == "1":  
        Utils.print_conversation()
        return jsonify(), 200
    if str(user_input).lower() == "2":
        Utils.print_analyze_data()    
        
        url='http://52.79.225.144:8080/sentiment/getData'
        json_data = json.dumps(Data.analyze_data[1:])
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
        content_list = [data["content"] for data in Data.conversation[1:] if data["role"] == "user" and data['username'] == id and data['username'] == id]
        
        merged_content = "\n".join(content_list)
        
        Analyze.extract_keywords(merged_content,id)
        Utils.print_key_word()
        
        url='http://52.79.225.144:8080/keyword/getKeyWord'
        filtered_data = [item for item in Data.key_word if (item.get("username") == id and item.get("time") == time)]
        json_data = json.dumps(filtered_data)
        print(json_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기      
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        Data.key_word.clear()
        return jsonify({'message': response}), 204
            
    if str(user_input).lower() == "4":
        content_list = [data["content"] for data in Data.conversation[1:] if data["role"] == "user" and data['username'] == id and data['time'] == time]
        merged_content = "\n".join(content_list)    
        try:
            Analyze.classify_document(merged_content,id)
            Utils.print_category()
        except Exception as e:
            print("오류 내용 : ", str(e))
        
        url='http://52.79.225.144:8080/keyword/getConcern'
        filtered_data = [item for item in Data.Category if item.get("username") == id]
        json_data = json.dumps(filtered_data)
        print(json_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
        print(response)
        if response.status_code == 200:  # 요청이 성공했을 경우
            print('데이터 전송 성공')
        else:
            print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
            print('오류 내용:', response.text)  # 오류 내용 출력
        Data.Category.clear()
        return jsonify({'message': response}), 204
    




    time = Utils.call_time()

    # 사용자 입력을 대화 기록에 추가
    Data.conversation.append({"role": "user", "content": user_input, "date": time, "username":id})
    
    messages_p =[{'role':Data.conversation[0]['role'] , 'content':Data.conversation[0]['content']}] + [{'role':item['role'] , 'content':item['content']} for item in Data.conversation if item['username'] == id]
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages_p,
    temperature=0.15,
    frequency_penalty=2.0,
    )
    print(messages_p)

    
    Analyze.analyze_sentiment(user_input,id)
    
    url='http://52.79.225.144:8080/sentiment/getData' # URL 변경 해줘야해요.......
    json_data = json.dumps(Data.analyze_data[-1])
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)  # POST 요청 보내기
    print(json_data)
    if response.status_code == 200:  # 요청이 성공했을 경우
        print('데이터 전송 성공')
    else:
        print('데이터 전송 실패:', response.status_code)  # 요청 실패 시 상태 코드 출력
        print('오류 내용:', response.text)  # 오류 내용 출력  
    

    # GPT의 응답을 대화 기록에 추가
    response = completion['choices'][0]['message']['content']
    Data.conversation.append({"role": "assistant", "content": response, "date": time, "username":id})
    

    print("\nGPT: " + response+"\n")  # GPT 응답 출력
    
    return jsonify({'message': response}), 200

if __name__ == '__main__':
    from waitress import serve
    print("server stating....")
    serve(app, host='0.0.0.0', port=8079)
    
    

