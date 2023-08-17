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

import App
import Config
import Data
import Utils



def sentiment_store(content,average_negative,average_positive,average_neutral,id):
    time = Utils.call_time()
    negative_value = average_negative
    positive_value = average_positive
    neutral_value = average_neutral
    Data.analyze_data.append({"content":content,"negative":negative_value,"positive":positive_value,"neutral":neutral_value,"date":time,"username":id})




def analyze_sentiment(content,id):
    
    okt = Okt()
    CheckSentence = False

    # 품사 태깅
    tagged = okt.pos(content)
    print(tagged)

    # 태그가 'Adjective' , 'Noun'+'Josa'+'Verb' , 'Noun'+'Verb'인 단어들만 추출
    adjectives_r = []
    for i in range(len(tagged)) :
        word, tag = tagged[i]
        adjectives = []
        
        if tag == 'Adjective':
            if i > 0 and (tagged[i-1][1] in ('Adverb','VerbPrefix')) : #부사, #접두사
                if(i > 1 and (tagged[i-2][1] in ('Noun') and not(tagged[i-2][0] in ('개','꺼져','뭐')))) :
                    adjectives.append(tagged[i-2][0]+tagged[i-1][0] + word)
                    CheckSentence = True
                elif(i > 2 and (tagged[i-2][1] in ('Josa') and (tagged[i-3][1] in ('Noun')))) :
                    adjectives.append(tagged[i-3][0]+tagged[i-2][0]+tagged[i-1][0] + word)
                    CheckSentence = True
                else :
                    adjectives.append(tagged[i-1][0] + word)
                    CheckSentence = True
                    
            elif(i > 0 and (tagged[i-1][1] in ('Noun') and not(tagged[i-2][0] in ('개','꺼져','뭐')))) :
                adjectives.append(tagged[i-1][0] + word)
                CheckSentence = True
                
            elif(i > 1 and (tagged[i-1][1] in ('Josa') and (tagged[i-2][1] in ('Noun')))) :
                adjectives.append(tagged[i-2][0] + tagged[i-1][0] + word)
                CheckSentence = True
                
            else :
                adjectives.append(word)
                CheckSentence = True
        
        
        if tag == 'Verb' and not(tagged[i-1][1] in ('Verb')):
            if (i > 0 and (tagged[i-1][1] in ('Adverb','VerbPrefix'))) :
                if(i > 1 and (tagged[i-2][1] in ('Noun'))) :
                    adjectives.append(tagged[i-2][0]+tagged[i-1][0] + word)
                    CheckSentence = True
                elif(i > 2 and (tagged[i-2][1] in ('Josa') and (tagged[i-3][1] in ('Noun')))) :
                    adjectives.append(tagged[i-3][0]+tagged[i-2][0]+tagged[i-1][0] + word)
                    CheckSentence = True
                else :
                    adjectives.append(tagged[i-1][0] + word)
                    CheckSentence = True
                    
            elif(i > 0 and (tagged[i-1][1] in ('Noun') and not(tagged[i-1][0] in ('개','꺼져','뭐')))) :
                adjectives.append(tagged[i-1][0] + word)
                CheckSentence = True
                
            elif(i > 1 and (tagged[i-1][1] in ('Josa') and (tagged[i-2][1] in ('Noun')))) :
                adjectives.append(tagged[i-2][0] + tagged[i-1][0] + word)
                CheckSentence = True
                
            else :
                adjectives.append(word)
                CheckSentence = True
                
            if(i < len(tagged)-2 and tagged[i+1][1] in ('Verb') and tagged[i+2][1] in ('Verb')) :
                adjectives.append(tagged[i+1][0] + tagged[i+2][0])
            elif(i < len(tagged)-1 and tagged[i+1][1] in ('Verb')) :
                adjectives.append(tagged[i+1][0])
        
                
        elif(i == 0 and tag == 'Verb'):
            if(tagged[i+1][1] in ('Verb')):
                adjectives.append(word + tagged[i+1][0])
            else :
                adjectives.append(word)
                
        if tag == 'Eomi' :
            if( i > 0 and (tagged[i-1][1] in ('Noun'))) :
                adjectives.append(tagged[i-1][0] + word)
                CheckSentence = True
                
        joined_string = ''.join(adjectives)
        if(joined_string !='') :
            adjectives_r.append(joined_string)
    print(adjectives_r)
    count = len(adjectives_r)
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


        for verb in adjectives_r:
            data = {
                "content": verb
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)
            rescode = response.status_code
            if rescode == 200:
                jsonD = response.json()
                print(f"감정 분석 결과 for '{verb}': ", jsonD)
                if((jsonD['document']['confidence']['neutral']) < 2) :
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
                
    sentiment_store(content,average_negative,average_positive,average_neutral,id)
            
    
        
        
        
def extract_keywords(text,id):
    key_path = 'service_account_key.json'
    time = Utils.call_time()
    
    # 서비스 계정 키를 사용하여 Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={'document': document})

    entity_names = [entity.name for entity in response.entities]
    top_keywords = Counter(entity_names).most_common(5)

    for keyword, count in top_keywords:
        Data.key_word.append({"keyword":keyword , "count":count, "date":time,"username":id})
    
    
        
        
            
        
        
        
        
def translate_text(text, source_language, target_language):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text



def classify_document(text,id):
    key_path = 'C:/Users/yechan/gpt-3/service_account_key.json'
    time = Utils.call_time()

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
            name = name.replace('/','')
            print(f'category: {name}, confidence: {category.confidence}')
            Data.Category.append({"category":name , "confidence":category.confidence,"date":time, "username":id})
    else:
        print('No categories found.')

