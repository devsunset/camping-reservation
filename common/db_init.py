# -*- coding: utf-8 -*-
##################################################
#
#                   db_init.py
#
##################################################

##################################################
#
# > seqlite3 install  && sqlite location PATH add
#
# > create table schema
#   - sqlite3 camping.db
#
##################################################

##################################################
# import

import logging
import logging.config
from os import path
import sqlite3

from common import config
from common import common
# import config
# import common

##################################################
# constant

# target db
TARGET_DB = config.TARGET_DB

# logging config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

# create logger
logger = logging.getLogger('camping-reservation')

common = common.Common()
##################################################

# db_init
def db_init():
    conn = None
    try:
        conn = sqlite3.connect(TARGET_DB)
        common.executeTxDB(conn, 'DROP TABLE IF EXISTS camping_meta')
        common.executeTxDB(conn, (
            'CREATE TABLE camping_meta (id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'day_name TEXT, day_of_week TEXT, site_name TEXT, remain_cnt TEXT, crt_dttm TEXT)'
        ))
        conn.commit()
    except Exception as e:
        logging.error(' Exception : %s' % e)
    finally:
        if conn is not None:
            conn.close()
    logger.warning('db_init completed...')


##################################################
# main
if __name__ == '__main__':
    db_init()
