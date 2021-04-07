import time
import pymysql.cursors
import queue
class Database:
    """Tietokantaluuokka, joka helpottaa tietokannan käsittelemistä. On useammalle säikeelle tarkoitettu (FLASK).

    """
    class ConnPool():
        def __init__(self, size, max_size, host, user, password, db, port):
            self.db_args = {
                "host" : host,
                "user" : user,
                "password" : password,
                "db" : db,
                "port" : port
            }
            self.max_size = max_size
            self.pool = queue.Queue(max_size)
            for i in range(size):
                conn = pymysql.connect(
                        host=self.db_args["host"],
                        user=self.db_args["user"],
                        password=self.db_args["password"],
                        db=self.db_args["db"],
                        port=self.db_args["port"]
                    )
                conn.autocommit(True)
                self.pool.put(
                    conn
                )
        def getConnection(self,):
            try:
                return self.pool.get_nowait()
            except queue.Empty:
                if self.pool.qsize < self.max_size:
                    conn = pymysql.connect(
                            host=self.db_args["host"],
                            user=self.db_args["user"],
                            password=self.db_args["password"],
                            db=self.db_args["db"],
                            port=self.db_args["port"]
                    )
                    conn.autocommit(True)
                    self.pool.put(
                        conn
                    )
                else:
                    raise Exception("Pool error")
        def putConnection(self, conn):
            if conn:
                conn.cursor().close()
            try:
                self.pool.put_nowait(conn)
            except queue.Full:
                print("Queue Full")
    def __init__(self, host, user, password, db, port):
        self.connection_pool = self.ConnPool(10, 800, host, user, password, db, port)
    def query(self, query, params=None):
        conn = self.connection_pool.getConnection()
        conn.ping(reconnect=True)
        if conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if params:
                    cursor.execute(query.format(**params))
                else:
                    cursor.execute(query)
        self.connection_pool.putConnection(conn)
    def getData(self, query, params=None):
        conn = self.connection_pool.getConnection()
        conn.ping(reconnect=True)
        data = None
        if conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if params:
                    cursor.execute(query.format(**params))
                else:
                    cursor.execute(query)
                data = cursor.fetchall()
        self.connection_pool.putConnection(conn)
        return data
    def escape(self, var):
        conn = self.connection_pool.getConnection()
        conn.ping(reconnect=True)
        data = conn.escape(var)
        self.connection_pool.putConnection(conn)
        return data