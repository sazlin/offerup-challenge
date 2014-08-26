import urllib
from celery import shared_task
import pHash
from django.core.exceptions import ObjectDoesNotExist

@shared_task
def checkForDuplicates(image_id):
    from image_upload_app.models import Image
    # download the image for the given image_id
    try:
        image = Image.objects.get(id=image_id)
    except ObjectDoesNotExist:
        print "[WARNING] Image {} does not exist.".format(image_id)
        return

    urllib.urlretrieve(image.fileName.url, 'temp_file')

    # generate phash
    image_phash = pHash.imagehash('temp_file')

    # could optionally delete temp_file here, but it's not necessary

    # search for similar phash's and set Duplicate field accordingly
    if Image.objects.filter(Hash=image_phash).exists():
        image.Duplicate = True
    else:
        image.Duplicate = False

    # store phash and save
    image.Hash = image_phash
    image.save()
    return
