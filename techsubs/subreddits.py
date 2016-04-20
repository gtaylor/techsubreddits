"""
This file contains our sub-reddit definitions.
"""

CATEGORY_PROGRAMMING_LANG = 'programming-language'
CATEGORY_CONTAINERIZATION = 'containerization'
CATEGORY_PLATFORM_INFRASTRUCTURE = 'platform-and-infrastructure'
CATEGORY_PROVISIONING_DEPLOYMENT = 'provisioning-and-deployment'

CATALOG = {}

# TODO: This is all placeholder. It would typically be the province of a DB,
# but I'm being really cheap and avoiding that bit of IO to GCP Datastore.
# Similarly, I don't want to pay for a full-blown RDBMS. We'll find a happy
# medium if this project sees the light of day in any meaningful capacity.


def add_programming_languages():
    subreddits = (
        'python', 'ruby', 'golang', 'java', 'cplusplus', 'csharp',
        'C_Programming', 'cpp', 'haskell', 'php', 'scala', 'javascript',
        'perl', 'swift', 'd_language', 'Rlanguage', 'matlab', 'dartlang',
        'ocaml', 'lisp', 'fsharp', 'erlang', 'lua', 'visualbasic', 'SQL',
        'rust',
    )
    for lang in subreddits:
        CATALOG[lang] = {'categories': [CATEGORY_PROGRAMMING_LANG]}


def add_containerization():
    subreddits = (
        'docker', 'kubernetes', 'mesos', 'coreos', 'openshift',
    )
    for lang in subreddits:
        CATALOG[lang] = {'categories': [CATEGORY_CONTAINERIZATION]}


def add_platform_and_infrastructure():
    subreddits = (
        'aws', 'googlecloud', 'AZURE', 'openstack',
    )
    for lang in subreddits:
        CATALOG[lang] = {'categories': [CATEGORY_PLATFORM_INFRASTRUCTURE]}


def add_provisioning_and_deployment():
    subreddits = (
        'vagrant', 'chef_opscode', 'Puppet', 'ansible', 'saltstack',
    )
    for lang in subreddits:
        CATALOG[lang] = {'categories': [CATEGORY_PROVISIONING_DEPLOYMENT]}


add_programming_languages()
add_containerization()
add_platform_and_infrastructure()
add_provisioning_and_deployment()
