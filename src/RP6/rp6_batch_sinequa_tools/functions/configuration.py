# coding=utf-8
import configparser
import logging
import os
import sys

from RP6.rp6_batch_sinequa_tools.functions.environment import get_environment


# Log Level variable initialization
# logLevel = 20  # logging.INFO = 20 / logging.DEBUG = 10


class Parameters:
    """Objects Parameters.

        Attributes:
            prettyFormat        Beautiful response.
            log                 Log request in log server.
            outputFormat        Choose response format (json/xml).
            echoRequest         Repeat request in response.
            logLevel            Level of standard log.
            sinequa_url         Sinequa URL.
            http_proxy          Http proxy.
            https_proxy         Https proxy.
            outputDocumentPath  Where the file are stored.
        """
    # Payload variables initialization
    prettyFormat = log = outputFormat = echoRequest = logLevel = None
    # Requests variables initialization
    sinequa_url = http_proxy = https_proxy = None
    # Repertoire de sortie du fichier d'extraction
    outputDocumentPath = None
    sinequa_collection_name = None
    sinequa_partitions_name = None
    sinequa_commands_name = None


def config_init(configfile):
    """
    Init configuration based on an ini file
    :param configfile: config filename
    :type: configfile: str
    :return: params : dict of parameters
    :rtype: class
    """
    params = Parameters()
    if os.getenv('FIP'):
        config_file_name = f"{os.getenv('FIP')}{os.sep}{configfile}"
    else:
        config_file_name = f"config{os.sep}{configfile}"
    config_section_name = get_environment()

    logging.info('Chargement du fichier de configuration %s', config_file_name)
    config = configparser.ConfigParser(allow_no_value=True)
    try:
        config.read_file(open(config_file_name, encoding="utf-8"))
    except IOError:
        logging.critical('Problème d\'accès au fichier de config %s', config_file_name)
        sys.exit(12)

    logging.info('Récupération de la configuration dans la section %s', config_section_name)

    logging.debug('\t+ config_section_name : %s', config_section_name)

    setattr(params, 'prettyFormat', config.getboolean(config_section_name, 'prettyFormat'))
    logging.debug('\t\t-> prettyFormat : %s', params.prettyFormat)
    setattr(params, 'log', config.getboolean(config_section_name, 'log'))
    logging.debug('\t\t-> log : %s', params.log)
    setattr(params, 'outputFormat', config.get(config_section_name, 'outputFormat'))
    logging.debug('\t\t-> outputFormat : %s', params.outputFormat)
    setattr(params, 'echoRequest', config.getboolean(config_section_name, 'echoRequest'))
    logging.debug('\t\t-> echoRequest : %s', params.echoRequest)

    setattr(params, 'logLevel', config.getint(config_section_name, 'logLevel'))
    logging.debug('\t\t-> logLevel : %s', params.logLevel)

    setattr(params, 'sinequa_url', config.get(config_section_name, 'sinequaUrl'))
    logging.debug('\t\t-> sinequa_url : %s', params.sinequa_url)
    try:
        setattr(params, 'sinequa_collection_name', config.get(config_section_name, 'sinequaCollectionName').split(','))
        logging.debug('\t\t-> sinequa_collection_name : %s', params.sinequa_collection_name)
    except configparser.NoOptionError:
        pass
    try:
        setattr(params, 'sinequa_partitions_name', config.get(config_section_name, 'sinequaPartitionsName').split(','))
        logging.debug('\t\t-> sinequa_partitions_name : %s', params.sinequa_partitions_name)
    except configparser.NoOptionError:
        pass
    try:
        setattr(params, 'sinequa_commands_name', config.get(config_section_name, 'sinequaCommandsName').split(','))
        logging.debug('\t\t-> sinequa_commands_name : %s', params.sinequa_commands_name)
    except configparser.NoOptionError:
        pass

    setattr(params, 'http_proxy', config.get(config_section_name, 'proxyHttp'))
    logging.debug('\t\t-> http_proxy : %s', params.http_proxy)
    setattr(params, 'https_proxy', config.get(config_section_name, 'proxyHttps'))
    logging.debug('\t\t-> https_proxy : %s', params.https_proxy)

    # Si outputDocumentPath existe en tant que variable d'environnement, alors on surcharge
    odp_tmp = config.get(config_section_name, 'outputDocumentPath')
    if os.getenv(odp_tmp):
        logging.debug('\t\t-> Le paramètre outputDocumentPath est une variable système.')
        logging.debug('\t\t-> %s -> %s', odp_tmp, os.getenv(odp_tmp))
        setattr(params, 'outputDocumentPath', os.getenv(odp_tmp))
    else:
        # Sinon on prends la valeur inscrite
        setattr(params, 'outputDocumentPath', odp_tmp)

    logging.debug('\t\t-> outputDocumentPath : %s', params.outputDocumentPath)

    # log_path = Path(rf"{config[config_section_name]['logPath']}")
    return params
