# coding=utf-8
"""
Sinequa Function
"""
import logging
import os
import sys

import requests
from requests_ntlm import HttpNtlmAuth


# Log Level variable initialization
# logLevel = 20  # logging.INFO = 20 / logging.DEBUG = 10
# logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)-8s - %(message)s')


def sinequa_request_where_clause(config_parameters) -> str:
    """
    Cette fonction construit une clause where pour la collection Sinequa.

    :param config_parameters: Les paramètres de configuration pour la collection Sinequa.
    :type config_parameters: class
    :return: La clause where construite pour la collection Sinequa.
    :rtype: str
    """
    # complétion de la requête SQL pour mettre plusieurs collections
    logging.debug("Construction de la clause where")
    logging.debug('\t -> Paramètre collection : %s', config_parameters.sinequaCollectionName)
    where_clause = 'where '
    first_clause = True
    sinequa_collection_list = config_parameters.sinequaCollectionName.split(',')
    if sinequa_collection_list:
        for sinequa_collection_name in sinequa_collection_list:
            if not first_clause:
                where_clause += ' or '
            where_clause += f"collection='{sinequa_collection_name}'"
            first_clause = False
    logging.debug('\t -> Clause where : %s', where_clause)
    return where_clause


def sinequa_request_executor(data_request: str, url_request: str, proxies_request: dict,
                             headers_request: dict, application_request: str,
                             auth_domain_request: str) -> requests.Response:
    """
    Execute la requête à travers les proxies sur l'URL demandée et renvoie la réponse.

    :param data_request: Les données de la requête.
    :type data_request: str
    :param url_request: L'URL de la requête.
    :type url_request: str
    :param proxies_request: Les proxies à utiliser pour la requête.
    :type proxies_request: dict
    :param headers_request: Les en-têtes de la requête.
    :type headers_request: dict
    :param application_request: Le nom de l'application Sinequa.
    :type application_request: str
    :param auth_domain_request: Le domaine d'authentification.
    :type auth_domain_request: str
    :return: La réponse de la requête.
    :rtype: requests.Response
    """
    request_response: requests.Response
    user = None
    password = None

    if headers_request is None:
        logging.warning("Attention aucun header n'est défini")

    if application_request is not None:
        # Récupération de l'utilisateur / mot de passe de sinequa
        logging.debug('\t+ Récupération des identifiants d\'authentification à %s', application_request)
        user = os.getenv(f"{application_request}_user")
        logging.debug('\t\t -> Utilisateur %s : %s', application_request, user)
        password = os.getenv(f"{application_request}_password")
        logging.debug('\t\t -> Mot de passe : %s', password)

    # TODO à revoir pour avoir une bonne logique
    # la requête doit être passée même si user / password = None
    # Exécution de la requête
    if user is not None and password is not None:
        session = requests.Session()

        # Si pas de domaine, alors pas d'authentification
        if auth_domain_request is not None:
            logging.debug('\t+ Lancement de la connexion au serveur')
            session.auth = HttpNtlmAuth(user, password, send_cbt=False)
            # Écrasement du domaine, car la librairie met le domaine en majuscule.
            session.auth.domain = auth_domain_request

        logging.debug("\t\t-> Exécution de la requête")
        request_response = session.post(url=url_request, proxies=proxies_request, headers=headers_request,
                                        data=data_request)
        logging.debug('\t\t -> Fin de la requête (%s)', request_response.status_code)
    else:
        logging.critical('Les paramètres %s_user / %s_password ne sont pas définis dans l\'environnement !',
                         application_request, application_request)
        sys.exit(12)
    return request_response


def call_sinequa_action(config_parameters, payload, proxies):
    """
    Appel de l'action Sinequa
    :param config_parameters: Les paramètres de configuration pour la collection Sinequa.
    :type config_parameters: class
    :param payload: Les données de la requête.
    :type payload: str
    :param proxies: Les proxies à utiliser pour la requête.
    :type proxies: dict
    :return: La réponse de la requête.
    :rtype: requests.Response
    """
    logging.info("Exécution de l'action")
    headers = {'Content-Type': 'application/json; charset=UTF-8', }
    response = sinequa_request_executor(data_request=payload,
                                        url_request=config_parameters.sinequa_url,
                                        proxies_request=proxies,
                                        application_request="Sinequa",
                                        auth_domain_request='AP.cdc.fr',
                                        headers_request=headers)
    return response
