from threading import Thread
from queue import Queue
from datetime import datetime as dt

import apsw

class SingleThreadOnly(object):
    def __init__(self, db):
        self.cnx = apsw.Connection(db) 
        self.cursor = self.cnx.cursor()
    def execute(self, req, arg=None):
        self.cursor.execute(req, arg or tuple())
    def select(self, req, arg=None):
        self.execute(req, arg)
        for raw in self.cursor:
            yield raw
    def close(self):
        self.cnx.close()

class MultiThreadOK(Thread):
    def __init__(self, db):
        super(MultiThreadOK, self).__init__()
        self.db=db
        self.reqs=Queue()
        self.start()
    def run(self):
        cnx = apsw.Connection(self.db) 
        cursor = cnx.cursor()
        while True:
            req, arg, res = self.reqs.get()
            if req=='--close--': break
            cursor.execute(req, arg)
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put('--no more--')
        cnx.close()
    def execute(self, req, arg=None, res=None):
        self.reqs.put((req, arg or tuple(), res))
    def select(self, req, arg=None):
        res=Queue()
        self.execute(req, arg, res)
        while True:
            rec=res.get()
            if rec=='--no more--': break
            yield rec
    def close(self):
        self.execute('--close--')

if __name__=='__main__':

    db_file = "test.db"
    table_name = "thread"

    multithread = True
    thread_size = 15
    
    if multithread:
        sql=MultiThreadOK(db_file)
    else:
        sql=SingleThreadOnly(db_file)

    # wipe all previous data
    sql.execute("delete from %s;" % table_name)
    sql.execute("delete from sqlite_sequence;")

    def insert_fn(name):
        records = [ r for r in sql.select("select count(*) from %s;" % table_name) ][0][0]
        # apsw not support datetime by default, cast ts to string
        ts = dt.now().strftime("%Y-%m-%d, %H:%M:%S.%f")
        sql.execute("INSERT INTO %s (task, records, ts) VALUES (?, ?, ?)" % table_name, ("thread-%02d" % name, records, ts))

    # start all jobs
    threads = list()
    for index in range(thread_size):
        x = Thread(target=insert_fn, args=(index,))
        threads.append(x)
        x.start()

    # wait all jobs done
    for index, thread in enumerate(threads):
        thread.join()

    sql.close()
    print('done')
