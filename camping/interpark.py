# -*- coding: utf-8 -*-
##################################################
#
#                   Interpark.py
#
##################################################

##################################################
# import

import datetime            
from dateutil.parser import parse
import json
import logging
import logging.config
from os import path
import time

from common import config
from common import common

##################################################
# constant

DAY_OF_WEEK = ['월', '화', '수', '목', '금', '토', '일']

##################################################
# delcare

# logging config
log_file_path = path.join(path.abspath(path.dirname(path.abspath(path.dirname(__file__)))), 'common/logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

comm = common.Common()

##################################################

class Interpark():
    def emptySiteCheck(self):
        site_name = config.INTERPARK_SITE_NAME.split(',')        
        site_check_url = config.INTERPARK_SITE_CHECK_URL.split(',')
        site_playseq = config.INTERPARK_SITE_PLAYSEQ.split(',')
        site_playseq_date = config.INTERPARK_SITE_PLAYSEQ_DATE.split(',')
        
        for i in range(len(site_name)):            
            # 1. get now date.            
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
            nowDate = parse(nowTime)
            # print(nowDate.date())

            # 2. playseq_date convert to date.
            playseq_date = parse(site_playseq_date[i])
            # print(playseq_date.date())

            # 3. now date - playseq_date  - get diff day
            date_diff = nowDate.date() - playseq_date.date()
            # print(date_diff.days)

            # 4. get current playseq
            current_playseq = int(site_playseq[i]) + date_diff.days
            # print(playseq)

            # 5. next day check 
            current =  datetime.datetime.now()
            for  n in range (0,62):
                nextday = current  + datetime.timedelta(days=n)             
                dw = nextday.weekday()
                # print(current_playseq+n , nextday.strftime('%Y-%m-%d'),DAY_OF_WEEK[dw])
                # 6. CHECK_DAY check - Friday (4) , Saturday (5),  Sunday (6)
                if (config.CHECK_DAY.find(str(dw)) > -1 or config.HOLYDAY.find(nextday.strftime('%Y-%m-%d')) > -1) and notPreCheckAndExceptionCheck(nextday.strftime('%Y-%m-%d'),site_name[i]) :
                    # print(current_playseq+n , nextday.strftime('%Y-%m-%d'),DAY_OF_WEEK[dw])
                    # 7. empty site check & noti telegram & db save
                    checkEnd = checkSite(site_check_url[i],current_playseq+n,site_name[i],nextday.strftime('%Y-%m-%d'),DAY_OF_WEEK[dw])
                    if checkEnd :
                        break

        logger.warning('Interpark check ...')

def checkSite(url,playseq,site_name,day_name,day_of_week):
    try:
        # print(url,playseq,site_name,day_name)
        url = url.replace("#PLAYSEQ#",str(playseq))
        # print(url)
        jsonText = comm.getCrawling(url)
        # print(jsonText)
        jsonObj = json.loads(jsonText)
        data = jsonObj['data']
        remainSeat = data['remainSeat']
        if len(remainSeat):
            # print(site_name,day_name,day_of_week,remainSeat[0]['remainCnt'])
            # 7. empty site check & noti telegram & db save
            if remainSeat[0]['remainCnt'] > 0:
                sqlText = 'insert into camping_meta  (day_name,day_of_week,site_name,remain_cnt,crt_dttm)'
                sqlText += ' values ("'+day_name+'","'+day_of_week+'","'+site_name+'","'+str(remainSeat[0]['remainCnt'])+'","'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'")'
                comm.executeDB(sqlText)
                comm.send_telegram_msg(site_name+" : "+day_name+" : "+day_of_week+" : "+str(remainSeat[0]['remainCnt']))
            return False
        else:
            return True
    except Exception as e:
        logger.error(e)
        return False

def notPreCheckAndExceptionCheck(day_name,site_name):
    # aleady push send and db save check
    sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'"'
    df = comm.searchDB(sqlText)
    # print(day_name,site_name,len(df))
    if df is not None:
        if len(df):
            return False

    #천왕산가족캠핑장 매월 10일 오전 10:00 ~ 10:30은 skip
    if site_name == '천왕산가족캠핑장':
        if "31" == datetime.datetime.now().strftime('%d'):
            # print(datetime.datetime.now().strftime('%H%M'))
            if 1000<= int(datetime.datetime.now().strftime('%H%M')) <=1030:
                return False

    return True
                    


                
