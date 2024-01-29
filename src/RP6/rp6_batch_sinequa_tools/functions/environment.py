# coding=utf-8
"""
    Select environment based on server name (ICDC specific)
"""
import os
import logging


# Log Level variable initialization
# logLevel = 10  # logging.INFO = 20 / logging.DEBUG = 10
# logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)-8s - %(message)s')


def find_environment_section(bigram):
    """Détermine la section du fichier de configuration en fonction du bigramme du hostname"""
    switcher = {
        "DV": "DEVELOPPEMENT",
        "IN": "INTEGRATION",
        "RC": "RECETTE",
        "VA": "VALIDATION",
        "PR": "PRODUCTION",
    }
    return switcher.get(bigram, "DEFAULT")


def get_environment() -> str:
    """Récupère le type d'environnement en vue de positionner les variables issues du fichier de configuration"""
    host_name = os.environ['COMPUTERNAME']
    logging.info('Récupération du nom de la machine : %s', host_name)
    logging.info('Détermination de l\'environnement d\'exécution')
    environment_bigram = host_name[3:5]
    environment_section = find_environment_section(environment_bigram)  # Choix de la section
    logging.info('Environnement détecté : %s', environment_section)
    return environment_section
