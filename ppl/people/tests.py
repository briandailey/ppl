import unittest
import transaction

from pyramid import testing

from ppl.models import DBSession, Base

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            pass

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        self.assertEqual(1,1)

