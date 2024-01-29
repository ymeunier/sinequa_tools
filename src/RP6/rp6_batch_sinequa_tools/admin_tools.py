# coding=utf-8
import json
import logging
import re
import sys

from RP6.rp6_batch_sinequa_tools.functions.arguments import get_arguments
from RP6.rp6_batch_sinequa_tools.functions.configuration import config_init
from RP6.rp6_batch_sinequa_tools.functions.sinequa import call_sinequa_action, sinequa_request_executor

# Log Level variable initialization
logLevel = 20  # logging.INFO = 20 / logging.DEBUG = 10
logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)-8s - %(message)s')


def remove_action(action_uid_value: str, config_parameters):
    """
    Remove the action UID from the actionUID.txt file.

    :param action_uid_value: The action UID to be removed.
    :type action_uid_value: str
    :param config_parameters: An object containing the configuration parameters.
    :type config_parameters: class
    :return: None
    """
    with open(f'{config_parameters.outputDocumentPath}\\actionUID.txt', encoding="utf-8") as fp:
        lines = fp.readlines()
    with open(f'{config_parameters.outputDocumentPath}\\actionUID.txt', 'w', encoding="utf-8") as fp:
        for line in lines:
            if line.strip("\n") != action_uid_value:
                fp.write(line)
    fp.close()


def statistic_analyzer(word: str, action_uid_value: str, count: int, line: str):
    """

    :param word:
    :param action_uid_value:
    :param count:
    :param line:
    :return:
    """
    # Recherche des erreurs
    error_finder = line.find(word)
    if error_finder > 0:
        error_count = int(re.findall(r'\d+', str(line))[0])
        if error_count > 0:
            logging.warning('\t-> %s : %s', action_uid_value, line)
            count += 1
    return count


def start(config_parameters, program_arguments, proxies):
    """
    Execute the start action for the specified order.

    :param config_parameters: A class containing the configuration parameters.
    :type config_parameters: class
    :param program_arguments: A dict containing the program arguments.
    :type program_arguments: class
    :param proxies: A dict containing the proxies parameters
    :type proxies: dict
    :return: Higher return code of the action
    :rtype: int
    """
    return_code = ['0']
    result = None

    logging.info('Action = %s', program_arguments.action)
    if program_arguments.order[0] == 'partition':
        for partition in config_parameters.sinequa_partitions_name:
            if partition:
                logging.info('Traitement de la partition = %s', partition)
            # Payload start
            payload = json.dumps({
                "method": "operation.partitionStart",
                "partition": partition,
                "pretty": config_parameters.prettyFormat,
                "log": config_parameters.log,
                "output": config_parameters.outputFormat,
                "echoRequest": config_parameters.echoRequest
            })
            result = call_sinequa_action(config_parameters, payload, proxies)

    if program_arguments.order[0] == 'collection':
        for collection in config_parameters.sinequa_collection_name:
            if collection:
                logging.info('Traitement de la collection = %s', collection)
            # Payload start
            payload = json.dumps({
                "method": "operation.collectionStart",
                "collection": collection,
                "pretty": config_parameters.prettyFormat,
                "log": config_parameters.log,
                "output": config_parameters.outputFormat,
                "echoRequest": config_parameters.echoRequest
            })
            result = call_sinequa_action(config_parameters, payload, proxies)

    if program_arguments.order[0] == 'command':
        for command in config_parameters.sinequa_commands_name:
            if command:
                logging.info('Traitement de la commande = %s', command)
            # Payload start
            payload = json.dumps({
                "method": "operation.commandStart",
                "command": command,
                "pretty": config_parameters.prettyFormat,
                "log": config_parameters.log,
                "output": config_parameters.outputFormat,
                "echoRequest": config_parameters.echoRequest
            })
            result = call_sinequa_action(config_parameters, payload, proxies)

    if result.status_code == 200:
        json_result = json.loads(result.content)
        logging.info('L\'action s\'est bien terminée (%s)', result.status_code)
        if logging.getLevelName('debug'):
            logging.debug('\t-> Action UID : %s', json_result['ActionUid'])
        # Écriture de l'action UID dans le fichier
        with open(f'{config_parameters.outputDocumentPath}\\ActionUid.txt', 'a', encoding="utf-8") as file:
            file.write(json_result['ActionUid'] + "\n")
    else:
        logging.critical('Erreur lors de l\'action (%s)', result.status_code)
        return_code.append('12')
    return max(return_code)


def status(config_parameters, program_arguments, proxies):
    """
    Execute the control status of action.

    :param config_parameters: A class containing the configuration parameters.
    :type config_parameters: class
    :param program_arguments: A dict containing the program arguments.
    :type program_arguments: class
    :param proxies: A dict containing the proxies parameters
    :type proxies: dict
    :return: Higher return code
    :rtype: int
    """
    return_code = ['0']
    with open(f'{config_parameters.outputDocumentPath}\\ActionUid.txt', encoding="utf-8") as file:
        action_uid_values = file.readlines()
    action_uid_values = [s.rstrip() for s in action_uid_values]
    count_actions = len(action_uid_values)
    if count_actions == 0:
        logging.info('Aucune action à contrôler')
    else:
        logging.info('%s action(s) à contrôler', len(action_uid_values))
        for action_uid_value in action_uid_values:
            logging.info('Action UID : %s', action_uid_value)
            payload = json.dumps({
                "method": "operation.actionStatus",
                "action": program_arguments.order[0],
                "actionUID": action_uid_value,
                "pretty": config_parameters.prettyFormat,
                "log": config_parameters.log,
                "output": config_parameters.outputFormat,
                "echoRequest": config_parameters.echoRequest
            })
            logging.info('Vérification de l\'action %s', action_uid_value)
            headers = {'Content-Type': 'application/json; charset=UTF-8', }
            result = sinequa_request_executor(data_request=payload,
                                              url_request=config_parameters.sinequa_url,
                                              proxies_request=proxies,
                                              application_request="Sinequa",
                                              auth_domain_request='AP.cdc.fr',
                                              headers_request=headers)
            if result.status_code == 200:
                json_result = json.loads(result.content)
                if json_result['StatusFound'] is True and json_result['IsRunning'] is False:
                    if json_result['ActionExitCode'] == 0:
                        logging.info('L\'action %s est déjà terminée (%s)', action_uid_value, result.status_code)
                    else:
                        logging.warning('L\'action %s est déjà terminée (%s)', action_uid_value, result.status_code)
                    try:

                        for line in json_result['Stats'].splitlines():
                            count = 0
                            count = statistic_analyzer('error', action_uid_value, count, line)
                            count = statistic_analyzer('warning', action_uid_value, count, line)
                            if count == 0:
                                logging.info('\t-> %s : %s', action_uid_value, line)
                    except AttributeError:
                        pass
                    # purge du fichier actionUID_filename
                    # TODO : fichier texte dans le fichier de configuration ? ...et pourquoi pas une section ?
                    remove_action(action_uid_value, config_parameters)
                    return_code.append('0')
                if json_result['StatusFound'] is False and json_result['IsRunning'] is True:
                    logging.info('L\'action %s n\'a pas été trouvée', action_uid_value)
                    return_code.append('2')
                if json_result['StatusFound'] is True and json_result['IsRunning'] is True:
                    logging.info('L\'action %s est toujours en cours', action_uid_value)
                    return_code.append('2')
            else:
                logging.critical('Erreur lors de l\'action (%s)', result.status_code)
                return_code.append('12')
    return max(return_code)


def main():
    """
    Execute the start or status action based on the input parameters.
    :return: None
    """
    # On détermine les options d'appel et on y ajoute l'action
    program_arguments = get_arguments()
    if logging.getLevelName('debug'):
        logging.debug("Analyse des arguments reçus")
        logging.debug('\t-> Argument(s) reçu(s) : %s', program_arguments)

    # Lecture du fichier ini & forçage du niveau de log
    config_parameters = config_init(program_arguments.configfile[0])

    if logLevel != config_parameters.logLevel:
        logging.info('Changement du niveau de log. Passage de %s à %s', logLevel, config_parameters.logLevel)
        logger = logging.getLogger()
        logger.setLevel(config_parameters.logLevel)

    proxies = {'http': config_parameters.http_proxy, 'https': config_parameters.https_proxy}
    rc = 0

    # Si l'action est start
    if program_arguments.action[0] == "start":
        rc = start(config_parameters, program_arguments, proxies)

    # si l'action est status
    if program_arguments.action[0] == "status":
        rc = status(config_parameters, program_arguments, proxies)

    sys.exit(int(rc))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
