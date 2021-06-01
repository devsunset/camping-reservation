# -*- coding: utf-8 -*-
##################################################
#
#          camping-reservation system
#
##################################################

##################################################
#
# 개요 - 프로세스 설명
#
##################################################

##################################################
# import

from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import logging.config
from os import path

from common import config
from camping import interpark
from camping import gwangmyeong
from camping import epoc
from common import common

##################################################
# constant

# logging config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'common/logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

interpark = interpark.Interpark()
gwangmyeong = gwangmyeong.Gwangmyeong()
epoc = epoc.Epoc()

##################################################

# main process
def main_process():   

  # old data delete 
  sqlText = 'delete from camping_meta where datetime(substr(day_name,0,11)) < datetime ("'"now"'" ,"'"localtime"'")'
  common.Common().executeDB(sqlText)

# 도덕산캠핑장
try:
  if config.GWANGMYEONG_SITE_SESSION_VALID < 2:
      gwangmyeong.emptySiteCheck()
except Exception as e:
    logger.error(e)

# 천왕산가족캠핑장,수도권매립지캠핑장,공릉관광지가족캠핑장,평택소풍정원캠핑장,안산화랑오토캠핑장,인천두리캠핑장,한탄강오토캠핑장,경기도청소년수련원캠핑장안산,평택내리캠핑장
try:
  interpark.emptySiteCheck()
except Exception as e:
    logger.error(e)

# 이포보오토캠핑장
try:
  epoc.emptySiteCheck()
except Exception as e:
    logger.error(e)
  
#################################################
# main
if __name__ == '__main__':
    main_process()
    
    scheduler = BlockingScheduler()
    scheduler.add_job(main_process, 'interval', seconds=config.INTERVAL_SECONDS)
    
    try:
       scheduler.start()
    except Exception as err:
       logger.error(' main Exception : %s' % e)      

   