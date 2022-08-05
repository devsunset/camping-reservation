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


##################################################

# main process
def main_process():   
  # old data delete 
  sqlText = 'delete from camping_meta where datetime(substr(day_name,0,11)) < datetime ("'"now"'" ,"'"localtime"'")'
  common.Common().executeDB(sqlText)

# 도덕산캠핑장 (주석 처리 - 세션 생성한 서버로 호출 안하면 거부하게 처리 됨) 
  if config.GWANGMYEONG_SITE_SESSION_VALID < 2:
      gwangmyeong.emptySiteCheck()

# 인터파크
  # interpark.emptySiteCheck()
  
#################################################
# main
if __name__ == '__main__':
    main_process()
    scheduler = BlockingScheduler()
    scheduler.add_job(main_process, 'interval', seconds=config.INTERVAL_SECONDS)
    try:
       scheduler.start()
    except Exception as err:
       logger.error(' main Exception : %s' % err)      

   