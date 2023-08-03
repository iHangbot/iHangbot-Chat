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

import Analyze
import App
import Config
import Data


def call_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")
    return formatted_time


def print_conversation():
    for data in Data.conversation:
        print("role:", data["role"])
        print("content:", data["content"])
        print("date:", data["date"])
        print("username:", data["username"])
        print()
        
        

def print_analyze_data():
    for data in Data.analyze_data:
        print("Content:", data["content"])
        print("negative:", data["negative"])
        print("positive:", data["positive"])
        print("neutral:", data["neutral"])
        print("date:", data["date"])
        print("username:", data["username"])
        print()
        
        
        
def print_key_word():
    for item in Data.key_word:
        keyword = item["keyword"]
        count = item["count"]
        date = item["date"]
        username = item["username"]
        print(f"Keyword: {keyword}, count: {count}, Date : {date}, username : {username}")


def print_category():
    for item in Data.Category:
        category = item["category"]
        confidence = item["confidence"]
        date = item["date"]
        username = item["username"]
        print(f"Category: {category}, Confidence: {confidence}, date : {date}, username : {username}")


