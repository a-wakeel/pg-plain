import logging
import psycopg2
import psycopg2.extras

logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class Pg:
    def __init__(self):
        logger.debug('initializing postgres')
        self.host, self.port = None, None
        self.database, self.pool = None, None
        self.user, self.passwd = None, None
        self.conn, self.cursor = None, None

        logger.debug('Server Addr: {host}:{port}; Database: {db}; User: {user}; Password: {passwd}'.format(
            host=self.host, port=self.port,
            db=self.database, user=self.user, passwd=self.passwd
        ))

    def connect(self, conn_dict):
        """
        Connect to the database
        :param conn_dict: connection params dictionary
        :type conn_dict: dictionary
        """
        logger.debug('connecting to the database')

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
            self.conn = psycopg2.connect(conn_params)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.exception(e.message)

    def execute(self, query, params):
        """
        Execute query on the database
        :param params: query parameters
        :param query: database query
        :type query: str
        :return: boolean
        """
        logger.info('executing query')
        logger.debug('Cursor: {cursor}, Query: {query}'.format(
            cursor=self.cursor, query=query))

        try:
            if query.split()[0].lower() == 'select':
                self.cursor.execute(query, params)
                return self.cursor.fetchall()
            else:
                return self.cursor.execute(query, params)
        except Exception as e:
            logger.exception(e.message)
            return False

    def commit(self):
        """
        Commit changes to the database permanently
        :return: boolean
        """
        logger.debug('commiting changes to database')
        try:
            return self.conn.commit()
        except Exception as e:
            logger.exception(e.message)
            return False

    def close(self):
        """
        Close connection and cursor to the database
        :return: boolean
        """
        logger.debug('closing connection to database')
        try:
            self.cursor.close()
            return self.conn.close()
        except Exception as e:
            logger.exception(e.message)
            return False
