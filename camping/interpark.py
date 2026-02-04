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
SITE_NAME_CHUNWANG = '천왕산가족캠핑장'

##################################################
# delcare

# logging config
log_file_path = path.join(path.abspath(path.dirname(path.abspath(path.dirname(__file__)))), 'common/logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

comm = common.Common()

##################################################

def _collect_bookable_play_info(data_list, now_dt, site_name_i):
    """예약 가능 기간 내 play 항목만 필터하여 playInfo 리스트로 반환."""
    formatted = int(now_dt.strftime('%Y%m%d%H%M'))
    today_str = now_dt.strftime('%Y%m%d')
    is_chunwang = site_name_i == SITE_NAME_CHUNWANG
    result = []
    for x in data_list:
        if int(x['bookableDate']) <= formatted <= int(x['bookingEndDate']):
            if is_chunwang:
                result.append({'playSeq': x['playSeq'], 'playDate': x['playDate']})
            elif today_str != x['playDate']:
                result.append({'playSeq': x['playSeq'], 'playDate': x['playDate']})
    return result


class Interpark():
    def emptySiteCheck(self):
        site_name = config.INTERPARK_SITE_NAME.split(',')
        site_code = config.INTERPARK_SITE_CODE.split(',')
        site_check_day = config.INTERPARK_SITE_CHECK_DAY.split(',')
        seat_grade_list = config.INTERPARK_SITE_SEAT_GRADE.split(',')
        site_check_url = config.INTERPARK_SITE_CHECK_URL
        site_calendar = config.INTERPARK_SITE_CALENDAR

        now_dt = datetime.datetime.now()
        yyyymm = now_dt.strftime('%Y%m')
        y, m = now_dt.year, now_dt.month
        this_month_start = yyyymm + '01'
        this_month_end = yyyymm + str(calendar.monthrange(y, m)[1])
        next_first = (datetime.datetime(y, m, 1) + datetime.timedelta(days=32)).replace(day=1)
        next_month_start = next_first.strftime('%Y%m%d')
        next_month_end = next_month_start[:6] + str(calendar.monthrange(next_first.year, next_first.month)[1])

        for i in range(len(site_name)):
            check_url = site_check_url.replace('#INTERPARK_SITE_CODE#', site_code[i])
            cal_url_this = site_calendar.replace('#INTERPARK_SITE_CODE#', site_code[i]).replace('#START_DATE#', this_month_start).replace('#END_DATE#', this_month_end)
            cal_url_next = site_calendar.replace('#INTERPARK_SITE_CODE#', site_code[i]).replace('#START_DATE#', next_month_start).replace('#END_DATE#', next_month_end)

            play_info = []
            for cal_url in (cal_url_this, cal_url_next):
                try:
                    js = json.loads(comm.getCrawling(cal_url))
                    data = js.get('data', [])
                    play_info.extend(_collect_bookable_play_info(data, now_dt, site_name[i]))
                except (json.JSONDecodeError, KeyError):
                    pass

            now_time = now_dt.strftime('%Y%m%d')
            now_date = parse(now_time)

            if play_info and site_name[i] == SITE_NAME_CHUNWANG:
                play_info.insert(0, {'playSeq': play_info[0]['playSeq'], 'playDate': now_time})

            for p in play_info:
                playseq_date = parse(p['playDate'])
                dw = playseq_date.weekday()
                date_diff = playseq_date.date() - now_date.date()
                day_str = playseq_date.date().strftime('%Y-%m-%d')
                if (date_diff.days >= 0
                        and (str(dw) in site_check_day[i] or config.HOLYDAY.find(day_str) >= 0)
                        and notPreCheckAndExceptionCheck(day_str, site_name[i], DAY_OF_WEEK[dw])):
                    check_end = checkSite(check_url, p['playSeq'], site_name[i], day_str, DAY_OF_WEEK[dw], seat_grade_list[i], site_code[i])
                    if check_end:
                        break

        logger.warning('Interpark check ...')

def checkSite(url,playseq,site_name,day_name,day_of_week,seatGrades,site_code):
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
            # empty site check & noti telegram & db save
            for r in remainSeat:
                if checkExist(r['seatGrade'], seatGrades) and r['remainCnt'] > 0:
                    # sqlText = 'delete from camping_meta where day_name="'+day_name+'" and day_of_week = "'+day_of_week+'" and site_name = "'+site_name+'"'
                    # comm.executeDB(sqlText)

                    crt_dttm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql_text = (
                        "INSERT INTO camping_meta "
                        "(day_name, day_of_week, site_name, remain_cnt, crt_dttm) "
                        "VALUES (?, ?, ?, ?, ?)"
                    )
                    comm.executeDB(sql_text, (day_name, day_of_week, site_name, str(r['remainCnt']), crt_dttm))
                    link = config.INTERPARK_SITE_LINK + site_code

                    skip_days = config.FINAL_SKIP_DAY if site_name == SITE_NAME_CHUNWANG else config.SKIP_DAY
                    if skip_days.find(day_name) == -1:
                        msg = f"{site_name} : {day_name}:{r['seatGradeName']} : {day_of_week} : {r['remainCnt']}\n{link}"
                        comm.send_telegram_msg(msg)
            return False
        else:
            return True
    except Exception as e:
        logger.error(e)
        return False

def checkExist(seat_grade, seat_grades_str):
    allowed = set(seat_grades_str.split(':'))
    return seat_grade in allowed

def notPreCheckAndExceptionCheck(day_name, site_name, day_of_week):
    # 당일 날짜 예약은 12시 전까지만 체크
    now = datetime.datetime.now()
    if day_name == now.strftime('%Y-%m-%d'):
        if now.hour > 12:
            return False

    sql_text = (
        "SELECT id FROM camping_meta WHERE day_name=? AND site_name=? "
        "AND crt_dttm > datetime('now', 'localtime', '-5 minutes')"
    )
    df = comm.searchDB(sql_text, (day_name, site_name))
    if df is not None:
        if len(df):
            return False

    return True
