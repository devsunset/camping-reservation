# -*- coding: utf-8 -*-
##################################################
#
#                   common.py
#
##################################################

##################################################
# import

import bs4
from pandas import DataFrame
import datetime
import logging
import logging.config
import math
from os import path
import random
import requests
import sqlite3
import sys
import telegram
import asyncio
import unicodedata
import urllib3
import random
import time

from common import config
# import config

##################################################
# constant

# target db
TARGET_DB = config.TARGET_DB

##################################################
# delcare



# logging config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')


bot = telegram.Bot(token=config.TELEGRAM_TOKEN)

##################################################

import asyncio

class Common():
    # search sql query - select
    def searchDB(self, sqlText, sqlParam=None, targetDB=TARGET_DB):
        columns = []
        result = []
        try:
            conn = sqlite3.connect(targetDB)
            cur = conn.cursor()
            sql = sqlText
            if sqlParam == None:
                cur.execute(sql)
            else:
              if str(type(sqlParam)) == "<class 'tuple'>":                    
                cur.execute(sql, sqlParam)
              else:
                cur.executemany(sql,sqlParam)
            columns = list(map(lambda x: x[0], cur.description))
            result = cur.fetchall()
            df = DataFrame.from_records(data=result, columns=columns)
        finally:
          if conn is not None:
            conn.close()
        return df

    # execute sql query - insert/update/delete
    def executeDB(self, sqlText, sqlParam=None, targetDB=TARGET_DB):
        try:
          conn = sqlite3.connect(targetDB)
          cur = conn.cursor()
          sql = sqlText
          if sqlParam == None:
              cur.execute(sql)
          else:
              if str(type(sqlParam)) == "<class 'tuple'>":    
                cur.execute(sql, sqlParam)
              else:
                cur.executemany(sql,sqlParam)
          conn.commit()
        finally:
          if conn is not None:
            conn.close()
        return cur.lastrowid

    # search sql query - select
    def searchTxDB(self, conn, sqlText, sqlParam=None):
        columns = []
        result = []
        cur = conn.cursor()
        sql = sqlText
        if sqlParam == None:
            cur.execute(sql)
        else:
            if str(type(sqlParam)) == "<class 'tuple'>":    
                cur.execute(sql, sqlParam)
            else:
                cur.executemany(sql,sqlParam)
        columns = list(map(lambda x: x[0], cur.description))
        result = cur.fetchall()
        return DataFrame.from_records(data=result, columns=columns)

    # execute sql query - insert/update/delete
    def executeTxDB(self, conn, sqlText, sqlParam=None):
        cur = conn.cursor()
        sql = sqlText
        if sqlParam == None:
            cur.execute(sql)
        else:
            if str(type(sqlParam)) == "<class 'tuple'>":    
                cur.execute(sql, sqlParam)
            else:   
                cur.executemany(sql,sqlParam)
        return cur.lastrowid

    # telegram message send
    def send_telegram_msg(self, msg):
        try:
            # bot.deleteWebhook()
            # try:
            #     chat_id = bot.getUpdates()[-1].message.chat.id                
            # except Exception as e:
            #     chat_id = config.TELEGRAM_CHAT_ID
            # bot sendMessage
            logger.warn(msg)
            asyncio.run(bot.sendMessage(chat_id=config.TELEGRAM_CHAT_ID, text=msg))
           
        except Exception as e:
            # logger.error(' send_telegram_msg Exception : %s' % e)
            pass

    # log
    def log(self, msg, push_yn="Y"):
        if push_yn == 'Y':
            self.send_telegram_msg(msg)
            logger.warning(msg)
        else:
            logger.warning(msg)

    def getCrawling(self, url):
        html = ""
        try:
            # SSL 경고 및 사이퍼 설정 (기존 로직 유지)
            requests.packages.urllib3.disable_warnings()
            try:
                requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
                requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            except AttributeError:
                pass

            # 차단 회피를 위한 핵심 설정 1: 다양한 User-Agent 랜덤 선택
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/119.0.0.0'
            ]

            # 차단 회피를 위한 핵심 설정 2: 브라우저처럼 보이게 하는 필수 헤더들
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.google.com/', # 유입 경로 세탁
                'Connection': 'keep-alive'
            }

            # 차단 회피를 위한 핵심 설정 3: 요청 전 랜덤 지연 (0.5~1.5초)
            # 너무 일정한 속도로 요청하면 기계로 판단합니다.
            time.sleep(random.uniform(0.5, 1.5))

            # 세션을 사용하여 쿠키를 자동으로 관리 (단발성 requests.get보다 안전함)
            session = requests.Session()
            
            # 실제 요청 수행 (기존 로직에서 headers와 timeout 추가)
            resp = session.get(url, cookies=None, verify=False, headers=headers, timeout=10)
            
            # 상태 확인 및 결과 반환
            if resp.status_code == 200:
                html = resp.text
                # print(html) # 결과가 너무 길면 주석 처리하세요
            else:
                logger.error(f' 차단됨 또는 오류 발생 (Status Code: {resp.status_code})')

        except Exception as e:
            # 기존 logger 형식 유지
            logger.error(' getHttpsCrawling Exception : %s' % e)
            
        return html

    # crawling
    # def getCrawling(self, url):
    #     html = ""
    #     try:
    #         requests.packages.urllib3.disable_warnings()
    #         requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    #         requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    #     except AttributeError:
    #         # no pyopenssl support used / needed / available
    #         pass

    #     try:
    #         user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'

    #         proxies = {
    #             'http': 'http://43.202.154.212'
    #         }

    #         # resp = requests.get(url, cookies=None,verify=False,headers={'User-Agent': user_agent}, proxies=proxies)
    #         resp = requests.get(url, cookies=None,verify=False,headers={'User-Agent': user_agent})
    #         html = resp.text
    #         print(html)
    #     except Exception as e:
    #         logger.error(' getHttpsCrawling Exception : %s' % e)
    #     return html

    
    # def getCrawling(self, url):
    #     html = ""
    #     try:
    #         user_agent = 'Mozilla/5.0'
    #         # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
    #         # accept =  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    #         # accept_encoding = 'gzip, deflate, br'
    #         # accept_language = 'ko-KR,en-US;q=0.7,en;q=0.3'
    #         # cache_control = 'no-cache'
    #         # cookie = 'OAX=0+rEpGMCw9EABFcM; pcid=166112558612119550; _trs_id=eY144%3E%3F04204%3F5473; _ga_4SKTL7E8Q8=GS1.1.1692774311.9.1.1692775063.5.0.0; _ga=GA1.2.1467706746.1661125590; ab.storage.deviceId.cd97b079-ff05-4967-873a-324050c2a198=%7B%22g%22%3A%22a1907f53-257c-0c55-1180-db7f1efe1101%22%2C%22c%22%3A1661125590550%2C%22l%22%3A1692774322428%7D; cto_bundle=UTWrAF9yUmtFcldWa3AyV3IwbHNYcyUyRkNua3dObVNqTnBKUHRtJTJCZlpzVWhXdnJtVEdnaUJUaXFOQll2eDJEb1JQTzJhZGNuWllHam1Ydk1SUGhHSllQZGJkQ0xkYiUyRjJIeVZiRSUyQlFmbDVSTjR4eFppRVRFW??FFNytMYjVSeVpudz09Iiwic2lkIjoiSzFMT25xYnA0SDQzUGE0YmV1akhqcVI5VGtCNFdva2FVRXBKSWxjdk5aST0ifQ.SNGstZwKnzBLkEToDjR9teO_Es6rncs0wIG9-44UI1cCgBgsaYz2loHEAuJp4X960Aw9T9px--6GYz719wFeyqxDGvtIZiF-WxgaQhGWsoxZxLIQlRjszoI90XYRpVyP9e4oqMw7geA5oeQ-uhyfMsL5lqBwDQ5S-7kV5VNIk8VSGInhwMRYzRSGvUGNvd7ONnbZDhoJBQd4AOi962PCIGIKmNB0JbyeOHKetgArQ7UliGOFi47J_Iyy2NOikO6tcV5YYFaDnQUrsGCTPwI1L9DmRNVAUfk5IQrPniDQ2xVSONAxNoWoLU0KNOAmx1n69yV-sbI2p1ESWLvEPRk2LA; q_interparkID=GX1YZbxOxcMaQgoHvt7pCA%3D%3D; q_imfs_pcid=557391482322639895'
    #         # resp = requests.get(url,headers={'User-Agent': user_agent,'Accept':accept,'Accept-Encoding':accept_encoding,'Accept-Language':accept_language,'Cache-Control':cache_control,'Cookie':cookie})
           
    #         # session_obj = requests.Session()
    #         # resp = session_obj.get(url,headers={'User-Agent': user_agent})
    #         # resp = requests.get(url,headers={'User-Agent': user_agent})


    #         proxies = {
    #             'http': 'http://121.159.146.251'
    #         }

    #         # 요청 보내기
    #         resp = requests.get(url,headers={'User-Agent':user_agent}, proxies=proxies)


    #         html = resp.text
    #     except Exception as e:
    #         logger.error(' getCrawling Exception : %s' % e)
    #     return html

    # sert crawling
    def getSertCrawling(self, url, cookies=None):
        html = ""
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass

        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
            resp = requests.get(url, cookies=cookies,verify=False,headers={'User-Agent': user_agent})
            html = resp.text
        except Exception as e:
            logger.error(' getHttpsCrawling Exception : %s' % e)
        return html

##################################################
# main
if __name__ == '__main__':
    comm = Common()
    print('* send_telegram_msg : ', comm.send_telegram_msg(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : send_telegram_msg"))
    print()
    print('* log push_yn -> Y : ', comm.log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : Y", "Y"))
    print()
    print('* log push_yn -> N : ',  comm.log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : N", "N"))
    print()
    print('* getCrawling html : ', comm.getCrawling("https://devsunset.github.io/"))
    print()
    print('* getCrawling BeautifulSoup')
    html = comm.getCrawling("https://www.google.com/")
    bs = bs4.BeautifulSoup(html, 'html.parser')
    tags = bs.select('a')
    for i in range(len(tags)):
        txt = tags[i].get("href")
        print(txt)
