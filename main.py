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

from camping import interpark

##################################################
# constant

# logging config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'common/logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

interpark = interpark.Interpark()

##################################################

# main process
def main_process():   
  interpark.emptySiteCheck()

#################################################
# main
if __name__ == '__main__':
    main_process()
    
    #scheduler = BlockingScheduler()
    #scheduler.add_job(main_process, 'interval', seconds=config.INTERVAL_SECONDS)
    
    #try:
    #    scheduler.start()
    #except Exception as err:
    #    logger.error(' main Exception : %s' % e)      