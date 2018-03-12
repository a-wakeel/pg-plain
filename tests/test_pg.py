import logging
from unittest import TestCase
from pg_plain.pg import Pg


logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")


class TestPg(TestCase):
    def setUp(self):
        self.pg = Pg()

    # def tearDown(self):
    #     self.pg.close()

    def test_init_params(self):
        conn_params = self.pg.get_conn_params()
        self.assertEqual(conn_params["Host"], None, "incorrect initialized host")
        self.assertEqual(conn_params["Port"], None, "incorrect initialized port")
        self.assertEqual(conn_params["Database"], None, "incorrect initialized database name")
        self.assertEqual(conn_params["User"], None, "incorrect initialized user name")
        self.assertEqual(conn_params["Password"], None, "incorrect initialized password")

    def test_connect(self):
        conn_params = {
            "Host": "localhost",
            "Port": 5432,
            "Database": "postgres",
            "User": "postgres",
            "Password": "123445"
        }

        with self.assertRaises(Exception) as context:
            self.pg.connect(conn_params)

        self.assertTrue('could not connect to the server' in context.exception)

        recvd_conn_params = self.pg.get_conn_params()

        self.assertEqual(recvd_conn_params["Host"], conn_params["Host"], "incorrect initialized host")
        self.assertEqual(recvd_conn_params["Port"], conn_params["Port"], "incorrect initialized port")
        self.assertEqual(recvd_conn_params["Database"], conn_params["Database"], "incorrect initialized database name")
        self.assertEqual(recvd_conn_params["User"], conn_params["User"], "incorrect initialized user name")
        self.assertEqual(recvd_conn_params["Password"], conn_params["Password"], "incorrect initialized password")

    def test_execute(self):
        self.fail()

    def test_commit(self):
        self.fail()

    def test_close(self):
        self.fail()
