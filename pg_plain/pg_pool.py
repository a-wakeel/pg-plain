import logging
import psycopg2
import psycopg2.extras

from psycopg2.pool import ThreadedConnectionPool

logger = logging.getLogger(__name__)


# Multi-threaded & Singleton wrapper to the postgres driver
class PgPool:
    def __init__(self):
        logger.debug('initializing postgres threaded pool')
        self.host, self.port = None, None
        self.database, self.pool = None, None
        self.user, self.passwd = None, None
        self.pool = None

        logger.debug('Server Addr: {host}:{port}; Database: {db}; User: {user}; Password: {passwd}'.format(
            host=self.host, port=self.port,
            db=self.database, user=self.user, passwd=self.passwd
        ))

    def create_pool(self, conn_dict):
        """
        Create a connection pool

        :param conn_dict: connection params dictionary
        :type conn_dict: dict
        """
        if conn_dict["Host"] is None:
            self.host = 'localhost'
        else:
            self.host = conn_dict["Host"]
        if conn_dict["Port"] is None:
            self.port = '5432'
        else:
            self.port = conn_dict["Port"]

        self.database = conn_dict["Database"]
        self.user = conn_dict["User"]
        self.passwd = conn_dict["Password"]

        conn_params = "host='{host}' dbname='{db}' user='{user}' password='{passwd}' port='{port}'".format(
            host=self.host, db=self.database, user=self.user, passwd=self.passwd, port=self.port
        )

        try:
            logger.debug('creating pool')
            self.pool = ThreadedConnectionPool(1, 50, conn_params)
        except Exception as e:
            logger.exception(e.message)

    def get_conn(self):
        """
        Get a connection from pool and return connection and cursor
        :return: conn, cursor
        """
        logger.debug('getting connection from pool')
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return conn, cursor
        except Exception as e:
            logger.exception(e.message)
            return None, None

    @staticmethod
    def execute_query(cursor, query, params):
        """
        Execute a query on database

        :param cursor: cursor object
        :param query: database query
        :type query: str
        :param params: query parameters
        :type params: tuple
        :return: query results or bool
        """
        logger.info('executing query')
        logger.debug('Cursor: {cursor}, Query: {query}'.format(
            cursor=cursor, query=query))

        try:
            if query.split()[0].lower() == 'select':
                cursor.execute(query, params)
                return cursor.fetchall()
            else:
                return cursor.execute(query, params)
        except Exception as e:
            logger.exception(e.message)
            return False

    # commit changes to db permanently
    @staticmethod
    def commit_changes(conn):
        """
        Commit changes to the databse permanently

        :param conn: connection object
        :return: bool
        """
        logger.debug('commiting changes to database')
        try:
            return conn.commit()
        except Exception as e:
            logger.exception(e.message)
            return False

    def put_conn(self, conn):
        """
        Put connection back to the pool

        :param conn: connection object
        :return: bool
        """
        logger.debug('putting connection {conn} back to pool'.format(conn=conn))
        try:
            return self.pool.putconn(conn)
        except Exception as e:
            logger.exception(e.message)
            return False

    def close_pool(self):
        """
        Closes connection pool
        :return: bool
        """
        logger.debug('closing connections pool')
        try:
            return self.pool.closeall()
        except Exception as e:
            logger.exception(e.message)
            return False