from threading import Thread
from Queue import Queue
import sqlite3

class MultiThreadSqlite(Thread):
    def __init__(self, db="subdomain.db"):
        super(MultiThreadSqlite, self).__init__()
        self.db=db
        self.reqs=Queue()
        self.start()
        self.__init_schema()

    def __init_schema(self):
        """
        init db schema
        """
        DB_SCHEMA = {
            "subdomain_info": """
                create table IF NOT EXISTS subdomain_info(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain text,
                    subdomain text,
                    ips text,
                    is_ping boolean,
                    nmap_info text,
                    is_alive boolean,
                    create_time TIMESTAMP,
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "dir_info": """
                create table IF NOT EXISTS dir_info(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subdomain text,
                    dir_path text,
                    http_status text,
                    scan_info text,
                    create_time TIMESTAMP,
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
        }
        for table, schema in DB_SCHEMA.items():
            self.execute(schema)

    def run(self):
        cnx = sqlite3.Connection(self.db) 
        cursor = cnx.cursor()
        while True:
            req, arg, res = self.reqs.get()
            print(req)
            if req=='--close--': break
            elif req=='--commit--': 
            	cnx.commit()
            	break
            # cursor.execute(req, arg)
            cursor.execute("insert into subdomain_info (domain, subdomain, ips, create_time) VALUES('guazi.com','qt.guazi.com','124.251.6.63','Tue Apr 16 18:41:57 2019')")
            # if res:
            #     for rec in cursor:
            #         res.put(rec)
            #     res.put('--no more--')
        print("--------------------no req in")
        print(cnx.execute("select count(1) from subdomain_info").fetchall())
        cnx.commit()
        cursor.close()
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

    def commit(self):
    	self.execute("--commit--")

    def close(self):
        self.execute('--close--')
