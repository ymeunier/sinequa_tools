# coding=utf-8
import unittest
from unittest import TestCase


class Test(TestCase):
    @unittest.skip("A corriger")
    def test_find_args_action(self):
        # FIXME : a finir !
        self.assertTrue(True)
