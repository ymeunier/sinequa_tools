# coding=utf-8
from unittest import TestCase
from RP6.rp6_batch_sinequa_tools.admin_tools import statistic_analyzer


class Test(TestCase):

    def test_statistic_analyzer_no_error(self):
        count = statistic_analyzer('erreur', 'action_uid', 0, '0 je cherche à remonter le nombre d\'erreur')
        self.assertEqual(count, 0)

    def test_statistic_analyzer_not_found(self):
        count = statistic_analyzer('motNonTrouvable', 'action_uid', 0, '0 je cherche à remonter le nombre d\'erreur')
        self.assertEqual(count, 0)

    def test_statistic_analyzer_with_error(self):
        with self.assertLogs(level='INFO') as cm:
            count = statistic_analyzer('erreur', 'action_uid', 0, '123 je cherche à remonter le nombre d\'erreur')
        self.assertEqual(cm.output, ['WARNING:root:	-> action_uid : 123 je cherche à remonter le nombre d\'erreur'])
        self.assertEqual(count, 1)

    def test_start(self):
        # FIXME : a finir !
        self.assertTrue(True)
