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
from camping import interpark as interpark_module
from common import common

##################################################
# constant

# logging config
log_file_path = path.join(path.dirname(
    path.abspath(__file__)), 'common/logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

interpark_crawler = interpark_module.Interpark()

##################################################

# main process
def main_process():
    # old data delete (날짜가 오늘 이전인 메타 데이터 삭제)
    sql_text = (
        "DELETE FROM camping_meta "
        "WHERE date(substr(day_name, 1, 10)) < date('now', 'localtime')"
    )
    common.Common().executeDB(sql_text)
    # 인터파크 빈자리 체크
    interpark_crawler.emptySiteCheck()


#################################################
# main
if __name__ == '__main__':
    main_process()
    scheduler = BlockingScheduler(timezone='Asia/Seoul')
    scheduler.add_job(main_process, 'interval',
                      seconds=config.INTERVAL_SECONDS)

    try:
        scheduler.start()
    except Exception as err:
        logger.error(' main Exception : %s' % err)
