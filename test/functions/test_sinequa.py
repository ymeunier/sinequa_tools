# coding=utf-8
import json
import os
import unittest
from unittest import TestCase
from unittest.mock import Mock
import emoji

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

    @unittest.skip
    def test_gros_delire(self):
        print(emoji.emojize(':koala:'))
        print(emoji.demojize(''))
        print(emoji.emojize(':rana:', language='it'))
        print(emoji.distinct_emoji_list(''))
        print(emoji.distinct_emoji_list('elfe_homme_peau_légèrement_mate'))
        print(emoji.emoji_list('elfe_homme_peau_légèrement_mate'))
        print("Elfe homme peau légèrement mate :", emoji.emojize(':elfe_homme_peau_légèrement_mate:', language='fr'))
        print("Drapeau Italie :", emoji.emojize(':drapeau_italie:', language='fr'))
        # ':mère_noël:'
        # ':mère_noël_peau_foncée:'
        # ':mère_noël_peau_claire:'
        # ':mère_noël_peau_mate:'
        # ':mère_noël_peau_moyennement_claire:'
        # ':mère_noël_peau_légèrement_mate:'
        # ':père_noël:'
        # ':père_noël_peau_foncée:'
        # ':père_noël_peau_claire:'
        # ':père_noël_peau_mate:'
        # ':père_noël_peau_moyennement_claire:'
        # ':père_noël_peau_légèrement_mate:'
        # ':drapeau_r.a.s._chinoise_de_macao:'
        # ':lion:'
        # ':balance:'
        # ':poissons:'
        # ':sagittaire:'
        # ':taureau:'
        # ':scorpion_zodiaque:'
        # ':bouton_nouveau:'
        # ':bouton_pas_bien:'
        # ':bouton_ok:'
        # ':ok:'
        # ':ok_peau_foncée:'
        # ':ok_peau_claire:'
        # ':ok_peau_mate:'
        # ':ok_peau_moyennement_claire:'
        # ':ok_peau_légèrement_mate:'
        # ':flèche_activé:'
        # ':groupe_sanguin_o:'
        # ':serpentaire:'
        # ':bouton_p:'
        # ':flèche_bientôt:'
        # ':bouton_sos:'
        # ':statue_de_la_liberté:'
        # ':t-rex:'
        # ':flèche_en_haut:'
        # ':bouton_vers_le_haut:'
        # ':bouton_vs:'
        # ':endormi:'

    @unittest.skip
    def test_gros_delire_2(self):
        bouton_japonais = [':bouton_accepter_en_japonais:', ':bouton_application_en_japonais:',
                           ':bouton_bonne_affaire_en_japonais:', ':château_japonais:',
                           ':bouton_félicitations_en_japonais:', ':bouton_félicitations_en_japonais:',
                           ':bouton_réduction_en_japonais:', ':poupées_japonaises:', ':bouton_gratuit_en_japonais:',
                           ':bouton_ici_en_japonais:', ':bouton_montant_mensuel_en_japonais:',
                           ':bouton_complet_en_japonais:', ':bouton_pas_gratuit_en_japonais:',
                           ':bouton_ouvert_pour_affaires_en_japonais:', ':bouton_note_pour_réussir_en_japonais:',
                           ':bureau_de_poste_japonais:', ':bouton_interdit_en_japonais:',
                           ':bouton_réservé_en_japonais:', ':bouton_secret_en_japonais:',
                           ':bouton_frais_de_service_en_japonais:', ':symbole_japonais_de_débutant:',
                           ':bouton_chambres_disponibles_en_japonais:']
        print("Nombre de bouton japonais : ", len(bouton_japonais))
        for japanese_button in bouton_japonais:
            print('\t ->', japanese_button.replace(':', '').replace('_', ' '), " : ",
                  emoji.emojize(japanese_button, language='fr'))

    @unittest.skip
    def test_gros_delire_3(self):
        drapeau = [':drapeau_israël:', ':drapeau_jamaïque:', ':drapeau_japon:', ':drapeau_jersey:',
                   ':drapeau_jordanie:', ':drapeau_kazakhstan:', ':drapeau_kenya:', ':drapeau_kiribati:',
                   ':drapeau_kosovo:', ':drapeau_koweït:', ':drapeau_kirghizstan:', ':drapeau_laos:',
                   ':drapeau_lettonie:', ':drapeau_liban:', ':drapeau_lesotho:', ':drapeau_liberia:', ':drapeau_libye:',
                   ':drapeau_liechtenstein:', ':drapeau_lituanie:', ':drapeau_luxembourg:', ':drapeau_madagascar:',
                   ':drapeau_malawi:', ':drapeau_malaisie:', ':drapeau_maldives:', ':drapeau_mali:', ':drapeau_malte:',
                   ':drapeau_îles_marshall:', ':drapeau_martinique:', ':drapeau_mauritanie:', ':drapeau_maurice:',
                   ':drapeau_mayotte:', ':drapeau_mexique:', ':drapeau_micronésie:', ':drapeau_moldavie:',
                   ':drapeau_monaco:', ':drapeau_mongolie:', ':drapeau_monténégro:', ':drapeau_montserrat:',
                   ':drapeau_maroc:', ':drapeau_mozambique:', ':drapeau_myanmar_(birmanie):', ':drapeau_namibie:',
                   ':drapeau_nauru:', ':drapeau_népal:', ':drapeau_pays-bas:', ':drapeau_nouvelle-calédonie:',
                   ':drapeau_nouvelle-zélande:', ':drapeau_nicaragua:', ':drapeau_niger:', ':drapeau_nigeria:',
                   ':drapeau_niue:', ':drapeau_île_norfolk:', ':drapeau_corée_du_nord:', ':drapeau_macédoine_du_nord:',
                   ':drapeau_îles_mariannes_du_nord:', ':drapeau_norvège:', ':drapeau_oman:', ':drapeau_pakistan:',
                   ':drapeau_palaos:', ':drapeau_territoires_palestiniens:', ':drapeau_panama:',
                   ':drapeau_papouasie-nouvelle-guinée:', ':drapeau_paraguay:', ':drapeau_pérou:',
                   ':drapeau_philippines:', ':drapeau_îles_pitcairn:', ':drapeau_pologne:', ':drapeau_portugal:',
                   ':drapeau_porto_rico:', ':drapeau_qatar:', ':drapeau_roumanie:', ':drapeau_russie:',
                   ':drapeau_rwanda:', ':drapeau_la_réunion:', ':drapeau_samoa:', ':drapeau_saint-marin:',
                   ':drapeau_arabie_saoudite:', ':drapeau_écosse:', ':drapeau_sénégal:', ':drapeau_serbie:',
                   ':drapeau_seychelles:', ':drapeau_sierra_leone:', ':drapeau_singapour:',
                   ':drapeau_saint-martin_(partie_néerlandaise):', ':drapeau_slovaquie:', ':drapeau_slovénie:',
                   ':drapeau_îles_salomon:', ':drapeau_somalie:', ':drapeau_afrique_du_sud:',
                   ':drapeau_géorgie_du_sud-et-les_îles_sandwich_du_sud:', ':drapeau_corée_du_sud:',
                   ':drapeau_soudan_du_sud:', ':drapeau_espagne:', ':drapeau_sri_lanka:', ':drapeau_saint-barthélemy:',
                   ':drapeau_sainte-hélène:', ':drapeau_saint-christophe-et-niévès:', ':drapeau_sainte-lucie:',
                   ':drapeau_saint-martin:', ':drapeau_saint-pierre-et-miquelon:',
                   ':drapeau_saint-vincent-et-les_grenadines:', ':drapeau_soudan:', ':drapeau_suriname:',
                   ':drapeau_svalbard_et_jan_mayen:', ':drapeau_suède:', ':drapeau_suisse:', ':drapeau_syrie:',
                   ':drapeau_sao_tomé-et-principe:', ':drapeau_taïwan:', ':drapeau_tadjikistan:', ':drapeau_thaïlande:',
                   ':drapeau_timor_oriental:', ':drapeau_togo:', ':drapeau_tokelau:', ':drapeau_tonga:',
                   ':drapeau_trinité-et-tobago:', ':drapeau_tristan_da_cunha:', ':drapeau_tunisie:',
                   ':drapeau_turquie:', ':drapeau_turkménistan:', ':drapeau_îles_turques-et-caïques:',
                   ':drapeau_tuvalu:', ':drapeau_îles_mineures_éloignées_des_états-unis:',
                   ':drapeau_îles_vierges_des_états-unis:', ':drapeau_ouganda:', ':drapeau_ukraine:',
                   ':drapeau_émirats_arabes_unis:', ':drapeau_royaume-uni:', ':drapeau_nations_unies:',
                   ':drapeau_états-unis:', ':drapeau_uruguay:', ':drapeau_ouzbékistan:', ':drapeau_vanuatu:',
                   ':drapeau_état_de_la_cité_du_vatican:', ':drapeau_venezuela:', ':drapeau_viêt_nam:',
                   ':drapeau_pays_de_galles:', ':drapeau_wallis-et-futuna:', ':drapeau_sahara_occidental:',
                   ':drapeau_yémen:', ':drapeau_zambie:', ':drapeau_zimbabwe:']
        print('Nombre de drapeaux : ', len(drapeau))
        for flag in drapeau:
            print('\t ->', flag.replace(':', '').replace('_', ' '), " : ", emoji.emojize(flag, language='fr'))

    @unittest.skip
    def test_gros_delire_4(self):
        print(emoji.LANGUAGES)
        print(emoji.STATUS)

    @unittest.skip
    def test_gros_delire_5(self):
        print(emoji.EMOJI_DATA.keys())

    @unittest.skip
    def test_gros_delire_6(self):
        for dictionnaire in emoji.EMOJI_DATA.values():
            if 'fr' in dictionnaire:
                print('\t-> ', dictionnaire['fr'].replace(':', '').replace('_', ' '), ' : ',
                      emoji.emojize(dictionnaire['fr'], language='fr'))
