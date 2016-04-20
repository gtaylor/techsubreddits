"""
This file contains our sub-reddit definitions.

TODO: This is all placeholder. It would typically be the province of a DB,
but I'm being really cheap and avoiding that bit of IO to GCP Datastore.
Similarly, I don't want to pay for a full-blown RDBMS. We'll find a happy
medium if this project sees the light of day in any meaningful capacity.
"""
import collections


CATEGORY_CONTAINERIZATION = 'containerization'
CATEGORY_DATABASES = 'databases'
CATEGORY_PLATFORM_INFRASTRUCTURE = 'platform-and-infrastructure'
CATEGORY_PROGRAMMING_LANG = 'programming-language'
CATEGORY_PROVISIONING_DEPLOYMENT = 'provisioning-and-deployment'

# noinspection PyArgumentList
CATEGORIES = collections.OrderedDict(sorted({
    CATEGORY_PROGRAMMING_LANG: {
        'slug': CATEGORY_PROGRAMMING_LANG,
        'human_name': 'Programming languages',
        'description': 'Subreddits dedicated to specific programming languages.',
    },
    CATEGORY_CONTAINERIZATION: {
        'slug': CATEGORY_CONTAINERIZATION,
        'human_name': 'Containerization',
        'description': 'Docker, rkt, Container orchestration, etc.'
    },
    CATEGORY_DATABASES: {
        'slug': CATEGORY_DATABASES,
        'human_name': 'Databases',
        'description': "It's where the data goes."
    },
    CATEGORY_PLATFORM_INFRASTRUCTURE: {
        'slug': CATEGORY_PLATFORM_INFRASTRUCTURE,
        'human_name': 'Platform and Infrastructure',
        'description': 'IaaS, PaaS, Bare metal, oh my!',
    },
    CATEGORY_PROVISIONING_DEPLOYMENT: {
        'slug': CATEGORY_PROVISIONING_DEPLOYMENT,
        'human_name': 'Provisioning and Deployment',
        'description': 'Provisioning, Configuration, and Deployment.'
    }
}.items()), key=lambda t: t[0])
if 'key' in CATEGORIES:
    del CATEGORIES['key']

# This is the primary catalog of Subreddits. The key is the Subreddit's
# name, whereas the value is some info about each.
CATALOG = {}

# Now we'll lazily define some functions to do the population of CATALOG,
# rather than explicitly writing it all out. We'll probably eventually
# have to write it all out if and when we add Subreddits to multiple categories.


def add_programming_languages():
    subreddits = (
        'python', 'ruby', 'golang', 'java', 'cplusplus', 'csharp',
        'C_Programming', 'cpp', 'haskell', 'php', 'scala', 'javascript',
        'perl', 'swift', 'd_language', 'Rlanguage', 'matlab', 'dartlang',
        'ocaml', 'lisp', 'fsharp', 'erlang', 'lua', 'visualbasic', 'SQL',
        'rust',
    )
    for lang in subreddits:
        CATALOG[lang] = {
            'slug': lang,
            'categories': [CATEGORY_PROGRAMMING_LANG],
        }


def add_containerization():
    subreddits = (
        'docker', 'kubernetes', 'mesos', 'coreos', 'openshift',
    )
    for lang in subreddits:
        CATALOG[lang] = {
            'slug': lang,
            'categories': [CATEGORY_CONTAINERIZATION],
        }


def add_platform_and_infrastructure():
    subreddits = (
        'aws', 'googlecloud', 'AZURE', 'openstack',
    )
    for lang in subreddits:
        CATALOG[lang] = {
            'slug': lang,
            'categories': [CATEGORY_PLATFORM_INFRASTRUCTURE],
        }


def add_provisioning_and_deployment():
    subreddits = (
        'vagrant', 'chef_opscode', 'Puppet', 'ansible', 'saltstack',
    )
    for lang in subreddits:
        CATALOG[lang] = {
            'slug': lang,
            'categories': [CATEGORY_PROVISIONING_DEPLOYMENT],
        }


def add_databases():
    subreddits = (
        'postgres', 'mariadb', 'mysql', 'cassandra', 'CouchDB', 'mongodb',
        'rethinkdb',
    )
    for lang in subreddits:
        CATALOG[lang] = {
            'slug': lang,
            'categories': [CATEGORY_DATABASES],
        }


add_programming_languages()
add_containerization()
add_platform_and_infrastructure()
add_provisioning_and_deployment()
add_databases()

# Sort the keys once we have all of them. Helps our views avoid doing that.
CATALOG = collections.OrderedDict(
    sorted(CATALOG.items(), key=lambda t: t[0].lower())
)


def is_valid_subreddit_category(category):
    """
    :param str category: A category name to validate.
    :rtype: bool
    :return: True if the given category is valid, False if not.
    """
    return category in CATEGORIES


def get_subreddits_in_category(category):
    """
    :param str category: The category to filter Subreddits by.
    :rtype: list
    :return: A list of Subreddit dicts matching the given category.
    """
    return [sr_dict for sr_dict in CATALOG.values()
            if category in sr_dict['categories']]
