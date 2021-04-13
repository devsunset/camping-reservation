# -*- coding: utf-8 -*-
##################################################
#
#                   gwangmyeong.py
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

class Gwangmyeong():
    def emptySiteCheck(self):
        site_name = config.GWANGMYEONG_SITE_NAME       
        site_check_url = config.GWANGMYEONG_SITE_CHECK_URL
        site_session_key = config.GWANGMYEONG_SITE_SESSION_KEY

        # 1. get now date.            
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        nowDate = parse(nowTime)
        # print(nowDate.date())

        # 2. get site reservation info.
        cookies = {'JSESSIONID': site_session_key}
        html = comm.getSertCrawling(site_check_url,cookies)

        # get now date.            
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        nowDate = parse(nowTime)
        # print(nowDate.date())

        # 3. session invalid check
        if html.find('LOGIN_FAIL_CNT') > -1:
            logger.error('jessionid is invalid')
            config.GWANGMYEONG_SITE_SESSION_VALID =  config.GWANGMYEONG_SITE_SESSION_VALID + 1
            comm.send_telegram_msg(site_name+" :  session invalid.")
            
            if config.GWANGMYEONG_SITE_SESSION_KEY.find('worker1') > -1:
                config.GWANGMYEONG_SITE_SESSION_KEY = config.GWANGMYEONG_SITE_SESSION_KEY.replace('worker1','worker2')
            else:
                config.GWANGMYEONG_SITE_SESSION_KEY = config.GWANGMYEONG_SITE_SESSION_KEY.replace('worker2','worker1')
        else:
        # 4. html parse - get site reservation  info
            bs = bs4.BeautifulSoup(html, 'html.parser')
            tags = bs.select('a')
            for i in range(len(tags)):
                txt = str(tags[i])
                if txt.find('doDraw') > -1:
                    # print(txt)
                    date_info =  txt[txt.find('(')+1:txt.find(')')].split(',')
                    # print(date_info)

                    # reservation date convert to date.
                    reservation_date = parse(date_info[1]+"-"+date_info[2]+"-"+date_info[0])
                    # print(reservation_date.date())

                    # reservation_date - now date = get diff day
                    date_diff =  reservation_date.date() - nowDate.date()
                    # print(date_diff.days)

                    dw = reservation_date.weekday()
                    # Future day check  AND GWANGMYEONG_SITE_CHECK_DAY check - Friday (4) , Saturday (5) AND HOLYDAY Check
                    
                    if date_diff.days > 0 and (config.GWANGMYEONG_SITE_CHECK_DAY.find(str(dw)) > -1 or config.HOLYDAY.find(reservation_date.strftime('%Y-%m-%d')) > -1) and notPreCheckAndExceptionCheck(reservation_date.strftime('%Y-%m-%d')+":"+date_info[3].replace("'","" ),site_name) :
                        # 5. empty site check & noti telegram & db save
                        if txt.find('잔여 데크: 0') == -1:
                             checkSite(site_name,reservation_date.strftime('%Y-%m-%d')+":"+date_info[3].replace("'","" ),DAY_OF_WEEK[dw],(txt[txt.find('잔여 데크:') +6:len(txt)-4]).replace(" ",""))

            if config.GWANGMYEONG_SITE_SESSION_VALID  == 1 :
                config.GWANGMYEONG_SITE_SESSION_VALID = 0
                comm.send_telegram_msg(site_name+" :  session valid.")

        logger.warning('Gwangmyeong check ...')
        
def checkSite(site_name,day_name,day_of_week,remain_cnt):
    try:
        sqlText = 'insert into camping_meta  (day_name,day_of_week,site_name,remain_cnt,crt_dttm)'
        sqlText += ' values ("'+day_name+'","'+day_of_week+'","'+site_name+'","'+remain_cnt+'","'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'")'
        comm.executeDB(sqlText)
        comm.send_telegram_msg(site_name+" : "+day_name+" : "+day_of_week+" : "+remain_cnt)
    except Exception as e:
        logger.error(e)

def notPreCheckAndExceptionCheck(day_name,site_name):
    # aleady push send and db save check
    if int('0000')<= int(datetime.datetime.now().strftime('%H%M')) <=int('0600'):
        sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(strftime("'"%Y-%m-%d 00:00:00"'", "'"now"'","'"localtime"'"))'
    else:
        sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(datetime ( "'"now"'", "'"localtime"'"), "'"-30 minutes"'")'
        
    df = comm.searchDB(sqlText)
    # print(day_name,site_name,len(df))
    if df is not None:
        if len(df):
            return False
    return True
                    


                
