# 본 코드는 BigKinds 사이트에서 API를 추출하여 제작되었습니다.
from datetime import datetime
import requests
import json
from .Log import Log
from tqdm import tqdm
from .Database import SQL
from .Preprocessing import DatetoString, CheckMySQLString

# 뉴스 카테고리 번호를 찾는 API와 검색 API의 요청 URL
CategoryApiUrl = 'https://www.bigkinds.or.kr/api/categories.do'
SearchApiUrl = 'https://www.bigkinds.or.kr/api/news/search.do'
DetailApiUrl = 'https://www.bigkinds.or.kr/news/detailView.do'

# 검색 API 사용시 Payload
payload = {
    'byLine': "",
    'dateCodes': [],
    'editorialIs': False,
    'incidentCodes': [],
    'indexName': "news",
    'isNotTmUsable': False,
    'isTmUsable': False,
    'mainTodayPersonYn': "",
    'networkNodeType': "",
    'newsIds': [],
    'searchFilterType': "1",
    'searchKey': "",
    'searchKeys': [{}],
    'searchScopeType': "1",
    'topicOrigin': "",
    'providerCodes': [],
}

# 검색 Api사용시 해더
# User-Agent가 존재하지 않을 시 서버에서 제대로된 응답을 보내지 않음. 
header = {
    'Content-Type': 'application/json',
    'Referer': 'https://www.bigkinds.or.kr/v2/news/index.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

# 뉴스 카테고리 API를 사용하여 카테고리 번호 추출
json_data = requests.post(CategoryApiUrl).json()
NewsCategory = dict()
NewsCategory['대분류'] = dict()
for i in json_data:
    NewsCategory[i['text']] = dict()
    NewsCategory['대분류'][i['text']] = i['id']
    for t in i['children']:
        NewsCategory[i['text']][t['text']] = t['id']

# 빅카인즈 뉴스 API 요청
def GetBigKindsNewsApi(category='경제', sort='date', startDate='2021-01-01', startNo=1, resultNumber=1000, endDate=str(datetime.today().strftime('%Y-%m-%d'))):
    Log('API 요청 시작')
    payload.update({
        'categoryId': list(NewsCategory[category].values()).insert(0, NewsCategory['대분류'][category]),
        'endDate': endDate,
        'resultNumber': resultNumber,
        'searchSortType': sort,
        'sortMethod': sort,
        'startDate': startDate,
        'startNo': startNo,
    })
    respond = requests.post(
        SearchApiUrl, data=json.dumps(payload), headers=header)
    Log('API 요청 완료')
    return respond.json()['resultList']

# 기사 불러오기
def GetArticle(docId=str):
    data = {'docId': docId, 'returnCnt': '1', 'sectionDiv': '1000'}
    response = requests.get(DetailApiUrl, params=data, headers=header)
    return response.json()['detail']['CONTENT']

# SQL DB에 저장하기
def SaveDB(res, sql: SQL):
    Log("DB 저장 시작")
    for item in tqdm(res):
        year = item['DATE'][0:4]
        month = item['DATE'][4:6]
        day = item['DATE'][6:8]
        DateTime = year + '-' + month + '-' + day + ' 00:00:00'
        Title = CheckMySQLString(item['TITLE'])
        Description = CheckMySQLString(GetArticle(item['NEWS_ID']))
        Link = CheckMySQLString(item['NEWS_ID'])
        sql.editDB("INSERT INTO `newsdata` (`title`, `link`, `description`, `pubDate`) VALUES ('{}', '{}', '{}', '{}');".format(
            Title, Link, Description, DateTime))
    Log("DB 저장 완료")
