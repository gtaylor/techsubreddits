"""
Functions for loading and setting configuration on the Flask app.
"""
import os


def populate_flask_config(app):
    """
    :param flask.app.Flask app: The Flask app to configure.
    """
    app.config['SITE_NAME'] = 'Tech Subreddit Tracker'
    server_software = os.environ.get('SERVER_SOFTWARE', '')
    if not server_software or server_software.startswith('Development'):
        app.config['IS_PRODUCTION'] = False
    else:
        app.config['IS_PRODUCTION'] = True
