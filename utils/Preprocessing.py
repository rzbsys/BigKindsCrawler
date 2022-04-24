import datetime
import re

stopwords = []
with open('utils/StopWords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read().splitlines()

def DatetoString(timeStr):
    time = datetime.datetime.strptime(timeStr, "%a, %d %b %Y %H:%M:%S %z")
    return time.strftime("%Y-%m-%d %H:%M:%S")

def CheckMySQLString(str):
    text = re.sub('|'.join(stopwords), ' ', str)
    # MySQL 오류 방지
    text = re.sub("'", " ", text)
    return text