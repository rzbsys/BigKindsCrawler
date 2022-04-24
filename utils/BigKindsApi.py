# 본 코드는 BigKinds 사이트에서 API를 추출하여 제작되었습니다.
from datetime import datetime
import requests
import json
from utils.Log import Log
from tqdm import tqdm
from utils.Database import SQL
from utils.Preprocessing import DatetoString, CheckMySQLString

# 뉴스 카테고리 번호를 찾는 API와 검색 API의 요청 URL
CategoryApiUrl = 'https://www.bigkinds.or.kr/api/categories.do'
SearchApiURL = 'https://www.bigkinds.or.kr/api/news/search.do'

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

def SaveDB(res, sql:SQL):
    Log("DB 저장 시작")
    for item in tqdm(res):
        year = item['DATE'][0:4]
        month = item['DATE'][4:6]
        day = item['DATE'][6:8]
        DateTime = year + '-' + month + '-' + day + ' 00:00:00'
        Title = CheckMySQLString(item['TITLE'])
        Description = CheckMySQLString(item['CONTENT'])
        Link = CheckMySQLString(item['PROVIDER_LINK_PAGE'])
        sql.editDB("INSERT INTO `newsdata` (`title`, `link`, `description`, `pubDate`) VALUES ('{}', '{}', '{}', '{}');".format(Title, Link, Description, DateTime))
    Log("DB 저장 완료")

def GetBigKindsNewsApi(category='경제', sort='date', startDate='2022-01-24', startNo=1, resultNumber=1000, endDate=str(datetime.today().strftime('%Y-%m-%d'))):
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
        SearchApiURL, data=json.dumps(payload), headers=header)
    return respond.json()['resultList']