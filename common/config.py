# -*- coding: utf-8 -*-
##################################################
#
#                   config.py
#
##################################################

# 프로그램 실행 주기
INTERVAL_SECONDS = 5

# target db
TARGET_DB = 'db/camping.db'

# telegram token
TELEGRAM_TOKEN = '2020114123:AAG557yWbe1g1e7ZFhZEsO6cn68_9HIozi8'

# telegram chat_id
TELEGRAM_CHAT_ID =-1001646770464

# day_of_week and holyday
HOLYDAY='2022-03-01'

# skip day
SKIP_DAY='2022-01-08,2022-01-15,2022-01-22,2022-01-29'

# site  interpark (seperate comma)
INTERPARK_SITE_NAME='천왕산가족캠핑장,수도권매립지캠핑장,공릉관광지가족캠핑장,평택소풍정원캠핑장,안산화랑오토캠핑장,한탄강오토캠핑장,경기도청소년수련원캠핑장안산,광주청소년야영장'
INTERPARK_SITE_CODE='21012652,20003504,20008285,20011252,20004246,16014399,20003920,19005586'
INTERPARK_SITE_CHECK_DAY='5,5,5,5,5,5,5,5'      # Friday (4) , Saturday (5),  Sunday (6)
INTERPARK_SITE_SEAT_GRADE='1,1:2,1,1:2,1,1:2,1,2'
INTERPARK_SITE_NOT_CHECK_DAY_TIME='10:10,15:14,15:11,15:10,01:13,01:13,27:14,18:14'

INTERPARK_SITE_CHECK_URL='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq/PlaySeq/#PLAYSEQ#/REMAINSEAT'
INTERPARK_SITE_CALENDAR='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq?endDate=#END_DATE#&goodsCode=#INTERPARK_SITE_CODE#&page=1&pageSize=1550&preSale=false&startDate=#START_DATE#'
INTERPARK_SITE_LINK='https://tickets.interpark.com/goods/'

# site Gwangmyeong
GWANGMYEONG_SITE_NAME='도덕산캠핑장'
GWANGMYEONG_SITE_CHECK_URL='https://reserve.gmuc.co.kr/user/camp/campReservation.do?menu=d&menuFlag=C'
GWANGMYEONG_SITE_CHECK_DAY='5' # Friday (4) , Saturday (5)
GWANGMYEONG_SITE_SESSION_KEY='A1195C1DEA8DFD2B0E1D4CB1142A20D2.worker2'
GWANGMYEONG_SITE_SESSION_VALID = 0
GWANGMYEONG_SITE_LINK='https://reserve.gmuc.co.kr/mobile/login/login.do?menuFlag=C'

# site Epoc
EPOC_SITE_NAME='이포보오토캠핑장'
EPOC_SITE_CHECK_URL='https://forest.maketicket.co.kr/event/event.do?command=event_view_schedule_list&idkey=5M7650&gd_seq=GD62&start=20210530&end=20210711'
EPOC_SITE_CHECK_DAY='5' # Friday (4) , Saturday (5)
EPOC_SITE_SESSION_KEY='D86E4DCDDE8BFB039ACFCF6A1BD25023'