from techsubs import app


API_BUCKET_NAME = 'www.techsubreddits.com'
if app.config['IS_PRODUCTION']:
    API_BUCKET_PATH = 'api'
else:
    API_BUCKET_PATH = 'dev/api'
