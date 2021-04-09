# -*- coding: utf-8 -*-
##################################################
#
#                   Interpark.py
#
##################################################

##################################################
# import

import calendar
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
        site_code = config.INTERPARK_SITE_CODE.split(',')        
        site_check_day = config.INTERPARK_SITE_CHECK_DAY.split(',')   
        site_not_chech_day_time = config.INTERPARK_SITE_NOT_CHECK_DAY_TIME.split(',')
        seatGrade= config.INTERPARK_SITE_SEAT_GRADE.split(',')

        site_check_url = config.INTERPARK_SITE_CHECK_URL
        site_calendar = config.INTERPARK_SITE_CALENDAR        

        thisMonth_startDate  = datetime.datetime.now().strftime('%Y%m')+"01"
        thisMonth_endDate  = datetime.datetime.now().strftime('%Y%m')+str(calendar.monthrange(int(datetime.datetime.now().strftime('%Y')),int(datetime.datetime.now().strftime('%m')))[1])
        dt = datetime.datetime(int(datetime.datetime.now().strftime('%Y')), int(datetime.datetime.now().strftime('%m')), 1)
        nextMonth_startDate = ((dt.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)).strftime('%Y%m%d')
        nextMonth_endDate = nextMonth_startDate[0:6]+str(calendar.monthrange(int(nextMonth_startDate[0:4]),int(nextMonth_startDate[4:6]))[1])

        for i in range(len(site_name)):
            check_url = site_check_url.replace('#INTERPARK_SITE_CODE#',site_code[i])
            cal_url_thisMonth = site_calendar.replace('#INTERPARK_SITE_CODE#',site_code[i]).replace('#START_DATE#',thisMonth_startDate).replace("#END_DATE#",thisMonth_endDate)
            cal_url_nextMonth = site_calendar.replace('#INTERPARK_SITE_CODE#',site_code[i]).replace('#START_DATE#',nextMonth_startDate).replace("#END_DATE#",nextMonth_endDate)

            playInfo = []

            jsonThisMonthText = comm.getCrawling(cal_url_thisMonth)
            jsonThisMonthObj = json.loads(jsonThisMonthText)
            dataThisMonth = jsonThisMonthObj['data']

            if len(dataThisMonth):
                for x in dataThisMonth:
                    playInfo.append( {'playSeq':x['playSeq'], 'playDate':x['playDate']})

            jsonNextMonthText = comm.getCrawling(cal_url_nextMonth)
            jsonNextMonthObj = json.loads(jsonNextMonthText)
            dataNextMonth = jsonNextMonthObj['data']
           
            if len(dataNextMonth):
                for x in dataNextMonth:
                    playInfo.append( {'playSeq':x['playSeq'], 'playDate':x['playDate']})

            nowTime = datetime.datetime.now().strftime('%Y%m%d')
            nowDate = parse(nowTime)

            if len(playInfo):
                if '천왕산가족캠핑장' == site_name[i]:
                    playInfo.insert(0,{'playSeq':int(playInfo[0]['playSeq'])-1,'playDate':nowTime})

            for p in playInfo:
                # print(p['playSeq'],p['playDate'])
                playseq_date = parse(p['playDate'])
                dw = playseq_date.weekday()
                date_diff = playseq_date.date() - nowDate.date()

                if date_diff.days > -1 and (site_check_day[i].find(str(dw)) > -1 or config.HOLYDAY.find(playseq_date.date().strftime('%Y-%m-%d')) > -1) and notPreCheckAndExceptionCheck(playseq_date.date().strftime('%Y-%m-%d'),site_name[i],site_not_chech_day_time[i]) :
                    # empty site check & noti telegram & db save
                    checkEnd = checkSite(check_url,p['playSeq'],site_name[i],playseq_date.date().strftime('%Y-%m-%d'),DAY_OF_WEEK[dw],seatGrade[i])
                    if checkEnd :
                        break

        logger.warning('Interpark check ...')

def checkSite(url,playseq,site_name,day_name,day_of_week,seatGrades):
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
            #  empty site check & noti telegram & db save
            for r in remainSeat:
                if checkExist(r['seatGrade'], seatGrades)  and r['remainCnt'] > 0:
                    sqlText = 'insert into camping_meta  (day_name,day_of_week,site_name,remain_cnt,crt_dttm)'
                    sqlText += ' values ("'+day_name+'","'+day_of_week+'","'+site_name+'","'+str(r['remainCnt'])+'","'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'")'
                    comm.executeDB(sqlText)
                    comm.send_telegram_msg(site_name+" : "+day_name+":"+r['seatGradeName'] +" : "+day_of_week+" : "+str(r['remainCnt']))
            return False
        else:
            return True
    except Exception as e:
        logger.error(e)
        return False

def checkExist(seatGrade, seatGrades):
    seatGrades = seatGrades.split(':')
    for x in seatGrades:        
        if seatGrade == x:   
            return True
    return False

def notPreCheckAndExceptionCheck(day_name,site_name,site_not_check_day_time):
    # aleady push send and db save check
    sqlText = 'select id from camping_meta where day_name="'+day_name+'" and site_name="'+site_name+'" and crt_dttm > datetime(datetime ( "'"now"'", "'"localtime"'"), "'"-10 minutes"'")'
    df = comm.searchDB(sqlText)
    if df is not None:
        if len(df):
            return False

    day_time = site_not_check_day_time.split(':')
     
    if day_time[0] == datetime.datetime.now().strftime('%d'):
        if int(day_time[1]+'00')<= int(datetime.datetime.now().strftime('%H%M')) <=int(day_time[1]+'05'):
            return False

    return True