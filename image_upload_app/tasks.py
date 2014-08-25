import os
import urllib
from celery import Celery

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BROKER_URL = 'sqs://%s:%s@%s' % (urllib.quote(AWS_ACCESS_KEY_ID, safe=''),
                               urllib.quote(AWS_SECRET_ACCESS_KEY, safe=''),
                               urllib.quote('sqs.us-west-2.amazonaws.com/093633342138/offerup_queue', safe=''))


app = Celery('tasks', broker=BROKER_URL)


@app.task
def checkForDuplicates(image_id):
    # get image for given image_id
    # generate phash
    # search for similar phash's
    # store phash and duplicate T/F value for given image_id
    return
