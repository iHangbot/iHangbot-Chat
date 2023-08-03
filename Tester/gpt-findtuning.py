import openai
import json

# OpenAI API 인증
openai.api_key = "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"

# 파인튜닝에 사용할 텍스트 데이터셋 로드
with open('dataset.txt', 'r') as f:
    dataset = f.read()

# 파인튜닝할 모델 설정
model_engine = "davinci"

# prompt.txt 파일에서 입력 텍스트 읽어오기
with open('prompt.txt', 'r') as f:
    prompt = f.read()

# OpenAI API를 사용하여 모델 파인튜닝
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    temperature=0.7,
    max_tokens=60,
    n=1,
    stop=None,
    frequency_penalty=0,
    presence_penalty=0,
    logprobs=None,
    echo=True,
    logit_bias=None,
    stop_sequence=None
)

# 파인튜닝 결과 출력
print(response.choices[0].text)