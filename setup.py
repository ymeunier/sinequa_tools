# coding=utf-8
import setuptools

setuptools.setup(

    # Métadonnées du paquet

    # à amender en fonction du contexte du projet

    name='rp6_batch_sinequa_tools',

    # Indiquez ici le numéro de version courant
    version='2.2.2',
    url='',
    license='proprietary',
    author='Equipe du projet rp6_batch_sinequa_tools',
    author_email='LD-MOE-Sinequa@caissedesdepots.fr',
    description='Outils d\'automatisation des tâches Sinequa',
    long_description=open('README.rst').read(),

    # Informations sur les points d'entrée de ce paquet

    # Permet de définir des noms de scripts qui seront disponibles dans l'environnement ou le paquet sera installé

    entry_points={
        "console_scripts": [
            'sinequa-admin-tools = RP6.rp6_batch_sinequa_tools.admin_tools:main',
        ]
    },

    # Informations de dépendances de ce paquet

    # Indiquez ici les dépendances du paquet
    # La précision de la version est facultative, mais recommandée
    # Sauf exception, cette liste ne doit pas rester vide
    install_requires=[
        'requests >= 2.31',
        'requests_ntlm',
        'sphinx'
        # ...
    ],

    # Option avancée
    # Indiquez ici des dépendances optionnelles permettant d'activer des fonctionnalités supplémentaires de votre paquet
    extras_require={
        # 'pdf_gen': ['reportlab>=3.5'],
        # ...
    },

    # Informations nécessaires au système de paquet

    # Sauf cas particulier, il n'est pas nécessaire de retoucher ces lignes
    packages=setuptools.find_namespace_packages(where='src', include=['RP6.*']),
    namespace_packages=['RP6'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
