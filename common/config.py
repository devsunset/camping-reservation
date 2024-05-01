# -*- coding: utf-8 -*-
##################################################
#
#                   config.py
#
##################################################

# 프로그램 실행 주기
INTERVAL_SECONDS = 10

# target db
TARGET_DB = 'db/camping.db'

# telegram token
TELEGRAM_TOKEN = '2020114123:AAG557yWbe1g1e7ZFhZEsO6cn68_9HIozi8'

# telegram chat_id
TELEGRAM_CHAT_ID =-1001646770464

# day_of_week and holyday
HOLYDAY='2024-05-05' 

# skip day 
SKIP_DAY='2024-05-05' 

# final skip day
FINAL_SKIP_DAY='2024-05-05' 

# site  interpark (seperate comma)
# INTERPARK_SITE_NAME='천왕산가족캠핑장,노을진(進)캠핑장,한탄강오토캠핑장,고양시킨텍스캠핑장,연천재인폭포오토캠핑장,공릉관광지가족캠핑장,평택내리캠핑장,평택소풍정원캠핑장,평택진위천유원지캠핑장,안성맞춤캠핑장'
# INTERPARK_SITE_CODE='21012652,22011899,21005592,22005895,22016459,20008285,20003499,20011252,21009223,20004468'
# INTERPARK_SITE_CHECK_DAY='5,5,5,5,5,5,5,5,5,5'      # Friday (4) , Saturday (5),  Sunday (6)
# INTERPARK_SITE_SEAT_GRADE='1,1:2,2,1,1,1,1,1:2,1,3'

INTERPARK_SITE_NAME='천왕산가족캠핑장,한탄강오토캠핑장,연천재인폭포오토캠핑장'
INTERPARK_SITE_CODE='21012652,21005592,22016459'
INTERPARK_SITE_CHECK_DAY='5,5,5'      # Friday (4) , Saturday (5),  Sunday (6)
INTERPARK_SITE_SEAT_GRADE='1,2,1'

INTERPARK_SITE_CHECK_URL='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq/PlaySeq/#PLAYSEQ#/REMAINSEAT'
INTERPARK_SITE_CALENDAR='https://api-ticketfront.interpark.com/v1/goods/#INTERPARK_SITE_CODE#/playSeq?endDate=#END_DATE#&goodsCode=#INTERPARK_SITE_CODE#&page=1&pageSize=1550&preSale=false&startDate=#START_DATE#'
INTERPARK_SITE_LINK='https://tickets.interpark.com/goods/'
