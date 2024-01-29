# coding=utf-8
import unittest
from unittest import TestCase


class Test(TestCase):
    @unittest.skip("A corriger")
    def test_config_init(self):
        # FIXME : a finir !
        self.assertTrue(True)
