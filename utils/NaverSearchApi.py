import requests
import os
from dotenv import load_dotenv
from .Database import SQL
from .Preprocessing import DatetoString, CheckMySQLString
from tqdm import tqdm
from .Log import Log

# 환경변수 불러오기
load_dotenv()
clientID = os.getenv('NAVER_CLIENT_ID')
clientKey = os.getenv('NAVER_CLIENT_KEY')

def SaveCSV(json, output='./output.csv'):
    try:
        # 기존에 파일이 존재할 시 제거
        if (os.path.exists(output)):
            os.remove(output)
    except OSError:
        raise Exception('기존 파일을 제거하는데 실패했습니다. 파일이 다른 프로그램에서 사용되고 있는지 확인해주세요.')

    # 파일 열기
    f = open(output, 'w', encoding='utf-8-sig')

    # 헤더 작성
    f.write("title, link, description, pubDate\n")

    # 데이터 작성
    for item in json['items']:
        f.write("{}, {}, {}, {}\n".format(item['title'], item['link'], item['description'], item['pubDate']))

    # 파일 닫기
    f.close()


def SaveDB(res, sql:SQL):
    Log("DB 저장 시작")
    for item in tqdm(res['items']):
        DateTime = DatetoString(item['pubDate'])
        Title = CheckMySQLString(item['title'])
        Description = CheckMySQLString(item['description'])
        Link = CheckMySQLString(item['link'])
        sql.editDB("INSERT INTO `newsdata` (`title`, `link`, `description`, `pubDate`) VALUES ('{}', '{}', '{}', '{}');".format(Title, Link, Description, DateTime))
    Log("DB 저장 완료")

# 네이버 검색 API 요청
def GetNaverNewsApi(query, output="json", display=100, start=1, sort="date"):
    display = str(display)
    start = str(start)
    url = "https://openapi.naver.com/v1/search/"\
          "news.{}"\
          "?"\
          "query={}"\
          "&display={}"\
          "&start={}"\
          "&sort={}".format(output, query, display, start, sort)

    headers = {'X-Naver-Client-Id': clientID,
               'X-Naver-Client-Secret' : clientKey}

    # API 전송
    Log("Naver API 요청 시작")
    res = requests.get(url, headers=headers)
    Log("Naver API 요청 완료")

    if (output == 'json'):
        return res.json()
    else:
        # 예외처리
        raise Exception("API의 output 형식이 잘못되었습니다.")