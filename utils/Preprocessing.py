import datetime
import re

# 불용어 사전 불러오기
stopwords = []
with open('utils/StopWords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read().splitlines()

def DatetoString(timeStr, input="%a, %d %b %Y %H:%M:%S %z", output="%Y-%m-%d %H:%M:%S"):
    time = datetime.datetime.strptime(timeStr, input)
    return time.strftime(output)

def CheckMySQLString(str):
    text = re.sub('|'.join(stopwords), ' ', str)
    # MySQL 오류 방지
    text = re.sub("'", " ", text)
    return text