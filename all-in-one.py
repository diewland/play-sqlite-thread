import logging
import threading
import sqlite3
from datetime import datetime as dt

db_file = "test.db"
table_name = "all_in_one"

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

# wipe all previous data
logging.info("Main    : deleted all previous data first")
conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute("delete from %s;" % table_name)
c.execute("delete from sqlite_sequence;")
conn.commit()
conn.close()

thread_size = 15

"""
STATELESS CONCEPT
    Each thread has its connection, not share with each others.
    Each record must NOT relate to other records.
    Because many threads do at the same/really close time.
    We cannot handle which come first, which come last.
"""
def insert_fn(name):
    logging.info("Thread %s: starting", name)

    # connect to db
    conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # find current total records
    c.execute("select count(*) from %s;" % table_name)
    records = c.fetchone()[0]

    # insert record
    c.execute("INSERT INTO %s (task, records, ts) VALUES (?, ?, ?)" % table_name, ("thread-%02d" % name, records, dt.now()))

    # commit & close db
    conn.commit()
    conn.close()

    logging.info("Thread %s: finishing", name)

# start all jobs
threads = list()
for index in range(thread_size):
    logging.info("Main    : create and start thread %d.", index)
    x = threading.Thread(target=insert_fn, args=(index,))
    threads.append(x)
    x.start()

# wait all jobs done
for index, thread in enumerate(threads):
    logging.info("Main    : before joining thread %d.", index)
    thread.join()
    logging.info("Main    : thread %d done", index)

print('done')
