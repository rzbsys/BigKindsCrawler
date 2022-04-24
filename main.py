# from utils.NaverSearchApi import GetNaverNewsApi as CrawlerApi, SaveDB
from utils.BigKindsApi import GetBigKindsNewsApi as CrawlerApi, SaveDB
from utils.Database import SQL
from dotenv import load_dotenv
import os

# 환경변수 설정
load_dotenv()
MysqlURL = os.getenv('MYSQL_URL')
MysqlUser = os.getenv('MYSQL_USER')
MysqlPassword = os.getenv('MYSQL_PASSWORD')
MysqlName = os.getenv('MYSQL_NAME')
SQL = SQL(MysqlUser, MysqlPassword, MysqlURL, MysqlName)

res = CrawlerApi()
SaveDB(res, SQL)
# SQL.EraseAllData()