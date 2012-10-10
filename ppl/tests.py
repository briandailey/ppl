import unittest
import transaction

from pyramid import testing

from .models import Session, initialize_sql

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
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'ppl')
