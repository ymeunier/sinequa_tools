# coding=utf-8
import json
import os
import unittest
from unittest import TestCase
from unittest.mock import Mock

from RP6.rp6_batch_sinequa_tools.functions.configuration import Parameters
from RP6.rp6_batch_sinequa_tools.functions.sinequa import sinequa_request_where_clause,sinequa_request_executor


class Test(TestCase):

    def test_sinequa_request_where_clause_multiple_collection(self):
        config_parameters = Parameters()
        config_parameters.sinequaCollectionName = "collection1,collection2"
        expected_output = "where collection='collection1' or collection='collection2'"
        self.assertEqual(sinequa_request_where_clause(config_parameters), expected_output, msg="Clause is not valid")

    def test_sinequa_request_where_clause_single_collection(self):
        config_parameters = Parameters()
        config_parameters.sinequaCollectionName = "collection1"
        expected_output = "where collection='collection1'"
        self.assertEqual(sinequa_request_where_clause(config_parameters), expected_output, msg="Clause is not valid")

    def test_sinequa_request_executor(self):
        # FIXME : A améliorer !
        mock_requests = Mock(sinequa_request_executor, return_value=b'{\r\n  "Action" : "collection",\r\n '
                                                                    b'"ActionUid" : '
                                                                    b'"F38C1EE262A14710A08B1EC1A41B6169",'
                                                                    b'\r\n  "methodresult" : "ok"\r\n}')
        data_request = json.dumps({
            "method": "method",
            "type": "type",
            "pretty": "prettyFormat",
            "log": "log",
            "output": "outputFormat",
            "echoRequest": "echoRequest"
        })
        os.environ["application_request_user"] = "application_request_user"
        os.environ["application_request_password"] = "application_request_password"
        url_request = "url_request"
        proxies_request = {'http': "http_proxy", 'https': "https_proxy"}
        headers_request = {''}
        application_request = "application_request"
        auth_domain_request = "auth_domain_request"
        expected_output = (b'{\r\n  "Action" : "collection",\r\n '
                           b'"ActionUid" : "F38C1EE262A14710A08B1EC1A41B6169",'
                           b'\r\n  "methodresult" : "ok"\r\n}')
        self.assertTrue(mock_requests)
        self.assertTrue(data_request)
        self.assertTrue(url_request)
        self.assertTrue(proxies_request)
        self.assertTrue(headers_request)
        self.assertTrue(application_request)
        self.assertTrue(auth_domain_request)
        self.assertTrue(expected_output)
        self.assertEqual(mock_requests(data_request, url_request, proxies_request, headers_request,
                                       application_request, auth_domain_request), expected_output,
                         msg="Incorrect response")

    @unittest.skip("A corriger")
    def test_call_sinequa_action(self):
        # FIXME : a finir !
        self.assertTrue(True)

            if 'fr' in dictionnaire:
                print('\t-> ', dictionnaire['fr'].replace(':', '').replace('_', ' '), ' : ',
                      emoji.emojize(dictionnaire['fr'], language='fr'))
