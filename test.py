import logging
import threading
import time
import sqlite3

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
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # find current total records
    c.execute("select count(*) from example;")
    records = c.fetchone()[0]

    # insert record
    c.execute("INSERT INTO example (task, records) VALUES (?, ?)", ("thread-%02d" % name, records))

    # commit & close db
    conn.commit()
    conn.close()

    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # wipe all previous data
    logging.info("Main    : deleted all previous data first")
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("delete from example;")
    c.execute("delete from sqlite_sequence;")
    conn.commit()
    conn.close()

    thread_size = 15

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
