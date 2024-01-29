# coding=utf-8
"""
    Arguments Constructor program
"""
import argparse
import configparser
import json
import logging
import os.path
import sys


# À revoir → Futur programme d'automatisation
# TODO : V2 une section argument_parser et une section argument_add, LogLevel a transmettre en paramètre

def find_args_action(action):
    """Vérifie que l'action envoyée est bien existante"""
    switcher = {
        "store": "store",
        "store_const": "store_const",
        "store_true": "store_true",
        "append": "append",
        "append_const": "append_const",
        "count": "count",
        "help": "help",
        "version": "version",
    }
    return switcher.get(action, None)


def get_arguments():
    """
    Arguments constructor based on an ini file

    :return: args: argparse object
    :rtype: arg
    """
    # TODO : Faire en sorte d'utiliser de base le fichier local ?
    # V1.3
    # print("Name : " + __name__)
    # print("Package : " + __package__)
    # print("File :  " + __file__)
    directory = str(os.path.split(sys.argv[0])[0])

    arguments_file = 'arguments-sinequa-admin-tools.ini'

    if os.getenv('FIP'):
        arguments_file_name = f"{os.getenv('FIP')}{os.sep}{arguments_file}"
    else:
        arguments_file_name = directory + os.sep + 'config' + os.sep + arguments_file

    logging.info('Chargement du fichier des arguments de la commande %s', arguments_file_name)
    arguments_parser = configparser.ConfigParser(allow_no_value=True)
    try:
        arguments_parser.read_file(open(arguments_file_name, encoding="utf-8"))
    except IOError:
        logging.critical('Problème d\'accès au fichier de configuration %s', arguments_file_name)
        sys.exit(12)

    defaults = arguments_parser.defaults()

    logging.debug('Affiche toutes les options de default %s', str(defaults))

    # Arguments : ArgumentParser
    # prog : The name of the program (default: os.path.basename(sys.argv[0]))
    # usage : The string describing the program usage
    #   (default: generated from arguments added to parser)
    # description : Text to display before the argument help (by default, no text)
    # epilog : Text to display after the argument help (by default, no text)
    # parents : A list of ArgumentParser objects whose arguments should also be included
    # formatter_class : A class for customizing the help output
    # prefix_chars : The set of characters that prefix optional arguments
    #   (default: ‘-‘)
    # form_prefix_chars : The set of characters that prefix files
    #   from which additional arguments should be read (default: None)
    # argument_default : The global default value for arguments (default: None)
    # conflict_handler : The strategy for resolving conflicting optionals (usually unnecessary)
    # add_help : Add a -h/--help option to the parser (default: True)
    # allow_abbrev : Allows long options to be abbreviated if the abbreviation is unambiguous.
    #   (default: True)
    # exit_on_error : Determines whether or not ArgumentParser exits with error info when an error
    #   occurs. (default: True)
    parser = argparse.ArgumentParser()

    # Liste les arguments
    for argument_name in defaults:
        logging.debug('\t -> argument %s : ', argument_name)
        value = json.loads(arguments_parser.defaults().get(argument_name))

        # Arguments : add_argument bloc

        arg_short_name = None
        arg_long_name = None
        arg_choices = None

        # Short name of the arguments (- + char)
        if len(str(value.get('shortname'))) == 1:
            arg_short_name = f"-{str(value.get('shortname'))}"
            logging.debug('\t\t -> arg_short_name : %s', arg_short_name)
        else:
            logging.critical('\t\t -> %s must be a uniq character', arg_short_name)

        # long name of the arguments (- + string)
        if value.get('longname') is not None:
            arg_long_name = f"--{str(value.get('longname'))}"
            logging.debug('\t\t -> arg_long_name : %s', arg_long_name)
        else:
            logging.warning('\t\t -> parameter longname not present')

        # required : Indicate whether an argument is required or optional
        # ==> True or False
        arg_required = False
        try:
            arg_required = bool(eval(value.get('required')))
        except ValueError:
            logging.critical('\t\t -> required must be a boolean')
        logging.debug('\t\t -> arg_required : %s', arg_required)

        # metavar : Alternate display name for the argument as shown in help
        arg_metavar = str(value.get('metavar'))
        logging.debug('\t\t -> arg_metavar : %s', arg_metavar)

        # nargs : Number of times the argument can be used
        arg_nargs = value.get('nargs')
        if arg_nargs in ['*', '+', 'argparse.REMAINDER']:
            pass
        elif arg_nargs.isdigit():
            arg_nargs = int(arg_nargs)
        else:
            raise argparse.ArgumentTypeError(
                'Type must be : int, ?, *, +, or argparse.REMAINDER')
        logging.debug('\t\t -> arg_nargs : %s', arg_nargs)

        # help : Help message for an argument
        arg_help = str(value.get('help'))
        logging.debug('\t\t -> arg_help : %s', arg_help)

        # type : Automatically convert an argument to the given type
        # ==> int, float, argparse.FileType('w'), or callable function
        arg_type = value.get('type')
        authorized_types = ['int', 'float', 'str']
        if arg_type not in authorized_types:
            raise argparse.ArgumentTypeError(
                'Type must be : int, float, argparse.FileType(\'w\'), or callable function')
        logging.debug('\t\t -> arg_type : %s', arg_type)

        # choices : Limit values to a specific set of choices
        # ==> ['foo', 'bar'], range(1, 10), or Container instance
        if value.get('choices') is not None:
            if not isinstance(value.get('choices'), (list, range)):
                raise argparse.ArgumentTypeError('Choices must be a list, a range, or a Container')
            arg_choices = value.get('choices')
            logging.debug('\t\t -> arg_choices : %s', arg_choices)

        # action : Specify how an argument should be handled
        # ==> 'store', 'store_const', 'store_true', 'append', 'append_const',
        #   'count', 'help', 'version'
        arg_action = find_args_action(value.get('action'))
        logging.debug('\t\t -> arg_action : %s', arg_action)

        # const Store a constant value
        arg_const = value.get('const')
        logging.debug('\t\t -> arg_const : %s', arg_const)

        # default : Default value used when an argument is not provided
        # ==> Defaults to None
        arg_default = value.get('default')
        logging.debug('\t\t -> arg_default : %s', arg_default)

        # destination : Specify the attribute name used in the result namespace
        # ==> Default = arg_long_name
        arg_destination = value.get('dest')
        logging.debug('\t\t -> arg_destination : %s', arg_destination)

        if arg_long_name is not None:
            parser.add_argument(arg_short_name, arg_long_name, type=eval(arg_type),
                                metavar=arg_metavar, required=arg_required, nargs=arg_nargs,
                                help=arg_help, action=arg_action, const=arg_const,
                                choices=arg_choices, default=arg_default, dest=arg_destination)
        else:
            parser.add_argument(arg_short_name, type=eval(arg_type),
                                metavar=arg_metavar, required=arg_required, nargs=arg_nargs,
                                help=arg_help, action=arg_action, const=arg_const,
                                choices=arg_choices, default=arg_default, dest=arg_destination)

    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(1)

    return args
