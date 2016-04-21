"""
This file contains our sub-reddit definitions.

TODO: This is all placeholder. It would typically be the province of a DB,
but I'm being really cheap and avoiding that bit of IO to GCP Datastore.
Similarly, I don't want to pay for a full-blown RDBMS. We'll find a happy
medium if this project sees the light of day in any meaningful capacity.
"""
import collections


# Use these instead of copy/pasta'ing the values around. Easier to mass
# rename and search on.
CATEGORY_CONTAINERIZATION = 'containerization'
CATEGORY_DATABASES = 'databases'
CATEGORY_SECURITY = 'security-and-hacking'
CATEGORY_NETWORKING = 'networking'
CATEGORY_OPERATING_SYSTEMS = 'operating-systems'
CATEGORY_PLATFORM_INFRASTRUCTURE = 'platform-and-infrastructure'
CATEGORY_PROGRAMMING_LANG = 'programming-language'
CATEGORY_OPERATIONS_ADMINISTRATION = 'operations-and-administration'
CATEGORY_PROGRAMMING_AND_COMP_SCI = 'programming-and-comp-sci'

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
    CATEGORY_NETWORKING: {
        'slug': CATEGORY_NETWORKING,
        'human_name': 'Networking',
        'description': 'Everything you never wanted to know about BGP.',
    },
    CATEGORY_OPERATING_SYSTEMS: {
        'slug': CATEGORY_OPERATING_SYSTEMS,
        'human_name': 'Operating Systems',
        'description': 'Operating systems, distributions, and other friends.',
    },
    CATEGORY_OPERATIONS_ADMINISTRATION: {
        'slug': CATEGORY_OPERATIONS_ADMINISTRATION,
        'human_name': 'Operations and Administration',
        'description': 'Provisioning, Configuration, Administration, and Deployment.'
    },
    CATEGORY_PLATFORM_INFRASTRUCTURE: {
        'slug': CATEGORY_PLATFORM_INFRASTRUCTURE,
        'human_name': 'Platform and Infrastructure',
        'description': 'IaaS, PaaS, Bare metal, oh my!',
    },
    CATEGORY_PROGRAMMING_AND_COMP_SCI: {
        'slug': CATEGORY_PROGRAMMING_AND_COMP_SCI,
        'human_name': 'Programming and Comp Sci',
        'description': 'Software Development, Comp Sci, self-improvement stuff.',
    },
    CATEGORY_SECURITY: {
        'slug': CATEGORY_SECURITY,
        'human_name': 'Security and Hacking',
        'description': 'Securing systems, intrusion detection, penetration testing, etc.'
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


def simple_add_to_category(category, subreddits):
    """
    A really cheezy way to mass add Subreddits to a category. In the future we
    may put certain Subreddits in multiple categories, which would cause this
    to be less fun.

    :param str category: One of the CATEGORY_* defines in this module.
    :param list subreddits: A list of Subreddits to add to the category.
    """
    for subreddit in subreddits:
        if not subreddit in CATALOG:
            CATALOG[subreddit] = {
                'slug': subreddit,
                'categories': [category],
            }
        else:
            CATALOG[subreddit]['categories'] += [category]

simple_add_to_category(
    category=CATEGORY_PROGRAMMING_LANG,
    subreddits=[
        'python', 'ruby', 'golang', 'java', 'cplusplus', 'csharp',
        'C_Programming', 'cpp', 'haskell', 'php', 'scala', 'javascript',
        'perl', 'swift', 'd_language', 'Rlanguage', 'matlab', 'dartlang',
        'ocaml', 'lisp', 'fsharp', 'erlang', 'lua', 'visualbasic', 'SQL',
        'rust', 'asm',
    ])
simple_add_to_category(
    category=CATEGORY_CONTAINERIZATION,
    subreddits=[
        'docker', 'kubernetes', 'mesos', 'coreos', 'openshift',
    ])
simple_add_to_category(
    category=CATEGORY_NETWORKING,
    subreddits=[
        'netsec', 'ccna', 'darknetplan', 'AskNetsec', 'wireless', 'networking',
        'HomeNetworking',
    ])
simple_add_to_category(
    category=CATEGORY_OPERATING_SYSTEMS,
    subreddits=[
        'linux', 'linux4noobs', 'ubuntu', 'bsd', 'osx', 'windows', 'unix',
    ])
simple_add_to_category(
    category=CATEGORY_PLATFORM_INFRASTRUCTURE,
    subreddits=[
        'aws', 'googlecloud', 'AZURE', 'openstack',
    ])
simple_add_to_category(
    category=CATEGORY_PROGRAMMING_AND_COMP_SCI,
    subreddits=[
        'programming', 'learnprogramming', 'ProgrammerHumor', 'dailyprogrammer',
        'coding', 'shittyprogramming',
    ])
simple_add_to_category(
    category=CATEGORY_OPERATIONS_ADMINISTRATION,
    subreddits=[
        'vagrant', 'chef_opscode', 'Puppet', 'ansible', 'saltstack',
        'iiiiiiitttttttttttt', 'sysadmin',
    ])
simple_add_to_category(
    category=CATEGORY_DATABASES,
    subreddits=[
        'postgres', 'mariadb', 'mysql', 'cassandra', 'CouchDB', 'mongodb',
        'rethinkdb',
    ])
simple_add_to_category(
    category=CATEGORY_SECURITY,
    subreddits=[
        'security', 'netsec', 'ComputerSecurity', 'compsec', 'AskNetsec',
        'hacking', 'pwned', 'SecurityAnalysis', 'securityCTF', 'HowToHack',
        'blackhat',
    ])

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
