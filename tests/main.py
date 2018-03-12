import unittest
from test_pg import TestPg
from test_pgPool import TestPgPool


def pg_test_suite():
    print('* executing pg test suite')
    pg_suite = unittest.TestSuite()
    pg_suite.addTest(TestPg('test_init_params'))
    pg_suite.addTest(TestPg('test_connect'))
    # pg_suite.addTest(TestPg('test_execute'))
    # pg_suite.addTest(TestPg('test_commit'))
    # pg_suite.addTest(TestPg('test_close'))
    return pg_suite


def pg_pool_test_suite():
    print('* executing pg pool test suite')
    pg_pool_suite = unittest.TestSuite()
    pg_pool_suite.addTest(TestPgPool('test_create_pool'))
    pg_pool_suite.addTest(TestPgPool('test_get_conn'))
    pg_pool_suite.addTest(TestPgPool('test_execute_query'))
    pg_pool_suite.addTest(TestPgPool('test_commit_changes'))
    pg_pool_suite.addTest(TestPgPool('test_put_conn'))
    pg_pool_suite.addTest(TestPgPool('test_close_pool'))
    return pg_pool_suite


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(pg_test_suite())
    #runner.run(pg_pool_test_suite())
