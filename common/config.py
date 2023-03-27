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
HOLYDAY='2023-05-05' 

# skip day 
SKIP_DAY='2023-04-01,2023-04-08,2023-04-22,2023-04-29,,023-05-06' 

# site  interpark (seperate comma)
INTERPARK_SITE_NAME='천왕산가족캠핑장,노을진(進)캠핑장,공릉관광지가족캠핑장,한탄강오토캠핑장,경기도청소년수련원캠핑장안산'
INTERPARK_SITE_CODE='21012652,22011899,20008285,21005592,20003920'
INTERPARK_SITE_CHECK_DAY='5,5,5,5,5'      # Friday (4) , Saturday (5),  Sunday (6)
INTERPARK_SITE_SEAT_GRADE='1,1:2,1,1:2,1'
INTERPARK_SITE_CHECK_URL='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq/PlaySeq/#PLAYSEQ#/REMAINSEAT'
INTERPARK_SITE_CALENDAR='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq?endDate=#END_DATE#&goodsCode=#INTERPARK_SITE_CODE#&page=1&pageSize=1550&preSale=false&startDate=#START_DATE#'
INTERPARK_SITE_LINK='https://tickets.interpark.com/goods/'

# site Gwangmyeong
GWANGMYEONG_SITE_NAME='도덕산캠핑장'
GWANGMYEONG_SITE_CHECK_URL='https://reserve.gmuc.co.kr/user/camp/campReservation.do?menu=d&menuFlag=C'
GWANGMYEONG_SITE_CHECK_DAY='5' # Friday (4) , Saturday (5)
GWANGMYEONG_SITE_SESSION_KEY='3F88CFCA61AA2D7E9E3EF5B0F89CEFCB.worker2'
GWANGMYEONG_SITE_SESSION_VALID = 0
GWANGMYEONG_SITE_LINK='https://reserve.gmuc.co.kr/mobile/login/login.do?menuFlag=C'
