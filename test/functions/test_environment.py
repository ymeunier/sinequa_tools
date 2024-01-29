# coding=utf-8
import unittest
from unittest import TestCase


class Test(TestCase):

    @unittest.skip("A corriger")
    def test_find_environment_section(self):
        # FIXME : a finir !
        self.assertTrue(True)
