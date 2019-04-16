"""
sqlite interface
"""

import sqlite3

class SqliteInterface(object):

    def __init__(self, DB_NAME="subdomain.db"):
        """
        init function
        """
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
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
            self.cursor.execute(schema)

    def save_subdomain(self, domain, subdomain, ips, scan_time):
        """
        save record into db
        """
        temp_sql = """
        insert into subdomain_info (domain, subdomain, ips, create_time) VALUES('%s','%s','%s','%s')
        """ % (domain, subdomain, ips, scan_time)
        # print(temp_sql)
        self.cursor.execute(temp_sql)

    def drop_connection(self):
        """
        close connection
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
