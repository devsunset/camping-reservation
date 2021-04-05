# -*- coding: utf-8 -*-
##################################################
#
#                   config.py
#
##################################################

# 프로그램 실행 주기
INTERVAL_SECONDS = 60

# target db
TARGET_DB = 'db/camping.db'

# telegram token
TELEGRAM_TOKEN = '1737609119:AAH51OD0QTW8X0kYgRaMd_dJMlwnXCC6qM4'

# telegram chat_id
TELEGRAM_CHAT_ID =-1001273432952
# TELEGRAM_CHAT_ID_1 = 1203202572
# TELEGRAM_CHAT_ID_2 = 1669531085

# day_of_week and holyday
CHECK_DAY='1456' # Friday (4) , Saturday (5),  Sunday (6)
HOLYDAY='2021-05-05,2021-05-19,2021-06-06,2021-08-15,2021-09-20,2021-09-21,2021-09-22,2021-10-03,2021-10-09,2021-12-25'

# site  interpark (seperate comma)
INTERPARK_SITE_NAME='천왕산가족캠핑장,수도권매립지캠핑장'
INTERPARK_SITE_CODE='20006668,20003504'
INTERPARK_SITE_CHECK_URL='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq/PlaySeq/#PLAYSEQ#/REMAINSEAT'
INTERPARK_SITE_CALENDAR='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq?endDate=#END_DATE#&goodsCode=#INTERPARK_SITE_CODE#&page=1&pageSize=1550&preSale=false&startDate=#START_DATE#'

# site Gwangmyeong
GWANGMYEONG_SITE_NAME='도덕산캠핑장'
GWANGMYEONG_SITE_CHECK_URL='https://reserve.gmuc.co.kr/user/camp/campReservation.do?menu=d&menuFlag=C'
GWANGMYEONG_SITE_SESSION_KEY='2E8EB4C80CF314B0E3B0287F2360940B.worker2'
GWANGMYEONG_SITE_SESSION_VALID = True
