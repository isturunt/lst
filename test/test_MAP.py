# -*- coding: utf-8 -*-
from unittest import TestCase

from lst.assessment.map import MAP
from lst.exceptions import MAPInitError

__author__ = 'isturunt'


class TestMAP(TestCase):

    def setUp(self):
        q_rule = lambda x: None
        u_rule = lambda x: None

    def test_get_question(self):
        pass

    def test_submit_result(self):
        pass

    def test_wrong_init_function_types(self):
        self.assertRaises(MAPInitError, MAP)
        self.assertRaises(MAPInitError, MAP, questioning_rule=1, updating_rule=lambda x1, x2, x3, x4: None)
        self.assertRaises(MAPInitError, MAP, questioning_rule=lambda x1, x2, x3, x4: None, updating_rule=1)

    def test_wrong_init_function_args_count(self):
        q_rule_good = lambda x1, x2, x3: None
        u_rule_good = lambda x1, x2, x3, x4: None
        for n in xrange(2):
            u_rule_bad = eval('lambda ' + ','.join(['x' + str(i) for i in range(n)]) + ": None")
            self.assertRaises(
                MAPInitError,
                MAP,
                questioning_rule=q_rule_good,
                updating_rule=u_rule_bad
            )
        q_rule_bad = lambda: None
        self.assertRaises(
            MAPInitError,
            MAP,
            questioning_rule=q_rule_bad,
            updating_rule=u_rule_good
        )
