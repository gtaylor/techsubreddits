import flask

from techsubs import app
from techsubs import subreddits
from techsubs.exceptions import NotFoundError


@app.route('/')
def landing_page():
    """
    App landing page.
    """
    return flask.render_template(
        'index.html', sr_categories=subreddits.CATEGORIES)


@app.route('/about', endpoint='about')
def about():
    """
    About page.
    """
    return flask.render_template('about.html')


@app.route('/suggest', endpoint='suggest')
def suggest():
    """
    A page that details how to suggest Subreddits or improvements.
    """
    return flask.render_template('suggest.html')


@app.route('/category/<subreddit_category>', endpoint='subreddit-category')
def subreddit_category(subreddit_category):
    """
    The index page for a Subreddit category.
    """
    if not subreddits.is_valid_subreddit_category(subreddit_category):
        raise NotFoundError('Invalid Subreddit category.')
    cat_subreddits = subreddits.get_subreddits_in_category(subreddit_category)
    return flask.render_template(
        'subreddit_index.html',
        subreddit_category=subreddits.CATEGORIES[subreddit_category],
        cat_subreddits=cat_subreddits)
