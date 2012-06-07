import datetime

from unittest import TestCase
from scripts.check_log_sent_to_johnsen import * 
from hamcrest import *
from monitor import *

from config import engine

class TestScript(TestCase):

    def setUp(self):
        CheckOK._shared_dict = None
        CheckJohnsen._shared_dict = None
        engine.execute("DELETE FROM RUNS;")

    def test_singleton(self):
        check = CheckOK()
        check.run()

        check2 = CheckOK()
        assert_that(check2.__dict__, is_(check.__dict__))

        check.set_frequency(12)
        assert_that(check2.__dict__, is_(check.__dict__))

    def test_script_execution(self):
        assert_that(CheckOK().run(), is_(Check.OK))

    def test_detection(self):
        assert_that(get_check_scripts(), has_item(CheckJohnsen))
        assert_that(len(get_check_scripts()), 2)
        
    def test_execution_msg(self):
        check = CheckOK()
        check.run()
	assert_that(check.last_exc, has_entry("name","CheckOK"))

	assert_that(check.last_exc, has_key("time"))
	assert_that(check.last_exc["time"], not_none())

        assert_that(check.last_exc, has_entry("status", Check.OK))

    def test_next_run_first_time(self):
        check_ok = CheckOK()
        check_johnson = CheckJohnsen()
        check_ok.set_frequency(5)
        check_johnson.set_frequency(1)

        assert_that(get_next_run(), has_items(CheckJohnsen, CheckOK))
 
        future = datetime.datetime.now() + datetime.timedelta(minutes=3)

        check_ok.run()
        assert_that(get_next_run(date_run=future), contains(CheckJohnsen))
