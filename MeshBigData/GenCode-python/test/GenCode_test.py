# coding=utf-8
# filename:name_tests.py

import nose.tools as tl
import GenCode_test


def setup():
    print('setup!')


def teardown():
    print('TEAR DOWN!')


def test_basic():
    print('I RAN!')
