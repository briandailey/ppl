import unittest
import transaction

from pyramid import testing

from ppl.models import Session, initialize_sql

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        initialize_sql(engine)
        with transaction.manager:
            pass

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_it(self):
        self.assertEqual(1, 1)

