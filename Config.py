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