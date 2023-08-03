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


# 대화 기록을 저장할 리스트
conversation = [
    {"role": "user", "content": "어린아이말투로 친절하게 꼭 반말로 대화해줘,","date":" ","username":"test123"}
]

# 감정 분석을 저장할 리스트
analyze_data =[
    {"content":"" ,"negative":"" ,"positive":"" ,"neutral":"" ,"date":" ","username":""}
]

key_word =[
    {"keyword":"" , "count":"","date":"","username":""}
]


Category =[
    {"category":"" , "confidence":"" , "date":"","username":""}
]
