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
        try:
            sqlText = 'drop table camping_meta'
            common.executeTxDB(conn, sqlText)
        except Exception as e:
            logging.error(' Exception : %s' % e)
            pass

        sqlText = 'create table camping_meta (id integer primary key autoincrement, day_name text, day_of_week text, site_name text, remain_cnt text, crt_dttm text)'
        common.executeTxDB(conn, sqlText)
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
