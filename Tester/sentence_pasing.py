from konlpy.tag import Okt
import requests
import json
import numpy as np

sentence ="나는 배가 고파서 예찬이랑 사과와 배를 먹고 제주도 행 배를 탔다."

okt = Okt()
CheckSentence = False

# 품사 태깅
tagged = okt.pos(sentence)
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
            "content": sentence
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