# -*- coding: utf-8 -*-
##################################################
#
#                   epoc.py
#
##################################################

##################################################
# import

import bs4
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

class Epoc():
    def emptySiteCheck(self):
        site_name = config.EPOC_SITE_NAME       
        site_check_url = config.EPOC_SITE_CHECK_URL

        # 1. get now date.            
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        nowDate = parse(nowTime)

        # 2. get site reservation info.
        cookies = {}
        html = comm.getSertCrawling(site_check_url,cookies)

        # get now date.            
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        nowDate = parse(nowTime)

        # 3. json parse - get site reservation  info
        jsonObject = json.loads(html)
        jsonArray = jsonObject.get("resultList")
        for list in jsonArray:
            # reservation date convert to date.
            reservation_date = parse(list.get('format_sd_date'))
            # reservation_date - now date = get diff day
            date_diff =  reservation_date.date() - nowDate.date()
           
            dw = reservation_date.weekday()
            # Future day check  AND EPOC_SITE_CHECK_DAY check - Friday (4) , Saturday (5) AND HOLYDAY Check
                
            if date_diff.days > 0 and (config.EPOC_SITE_CHECK_DAY.find(str(dw)) > -1 or config.HOLYDAY.find(reservation_date.strftime('%Y-%m-%d')) > -1) and notPreCheckAndExceptionCheck(reservation_date.strftime('%Y-%m-%d'),site_name,DAY_OF_WEEK[dw]) :
                # 5. empty site check & noti telegram & db save
                if list.get('reserve_ready_cnt') > 0:
                        checkSite(site_name,reservation_date.strftime('%Y-%m-%d'),DAY_OF_WEEK[dw],str(list.get('reserve_ready_cnt')))

        logger.warning('Epoc check ...')
        
def checkSite(site_name,day_name,day_of_week,remain_cnt):
    try:
        # sqlText = 'delete from camping_meta where day_name="'+day_name+'" and day_of_week = "'+day_of_week+'" and site_name = "'+site_name+'"'
        # comm.executeDB(sqlText)

        sqlText = 'insert into camping_meta  (day_name,day_of_week,site_name,remain_cnt,crt_dttm)'
        sqlText += ' values ("'+day_name+'","'+day_of_week+'","'+site_name+'","'+remain_cnt+'","'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'")'
        comm.executeDB(sqlText)
        comm.send_telegram_msg(site_name+" : "+day_name+" : "+day_of_week+" : "+remain_cnt)
    except Exception as e:
        logger.error(e)

def notPreCheckAndExceptionCheck(day_name,site_name,day_of_week):
    # aleady push send and db save check
    # if int('0000')<= int(datetime.datetime.now().strftime('%H%M')) <=int('0600'):
    #     sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(strftime("'"%Y-%m-%d 00:00:00"'", "'"now"'","'"localtime"'"))'
    # else:
    #     if day_of_week == "토":
    #         sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(datetime ( "'"now"'", "'"localtime"'"), "'"-30 minutes"'")'
    #     else:
    #         sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(datetime ( "'"now"'", "'"localtime"'"), "'"-360 minutes"'")'

    sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(datetime ( "'"now"'", "'"localtime"'"), "'"-5 minutes"'")'

    df = comm.searchDB(sqlText)
    # print(day_name,site_name,len(df))
    if df is not None:
        if len(df):
            return False
    return True
                    


                
