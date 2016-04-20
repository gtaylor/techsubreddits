import flask

from techsubs import app
from techsubs.bucket_populator import category_overview


@app.route('/api/category/<subreddit_category>/overview',
           endpoint='api-subreddit-category-overview')
def subreddit_category_overview(subreddit_category):
    # noinspection PyProtectedMember
    json = category_overview._generate_json(subreddit_category)
    return flask.Response(json, content_type='application/json')
