from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from image_upload_app.tasks import checkForDuplicates

def upload_image_to(instance, filename):
    from django.utils.timezone import now
    return 'images/{}/{}'.format(
        now().strftime("%Y%m%d%H%M%S"),
        filename)


class Image(models.Model):
    fileName = models.ImageField(upload_to=upload_image_to)
    Duplicate = models.NullBooleanField()
    Hash = models.CharField(max_length=72, blank=True)


@receiver(signal=post_save, sender=Image)
def image_post_save(sender, instance, created, *args, **kwargs):
    if created:
        print 'image created --> checking for dupes for ', instance.id
        checkForDuplicates.delay(instance.id)


@receiver(signal=post_delete, sender=Image)
def image_post_delete_(sender, instance, **kwargs):
    print 'image deleted --> removing file from s3 ', instance.id
    instance.fileName.delete(False)

    # The following two line also work
    # storage, name = instance.fileName.storage, instance.fileName.name
    # storage.delete(name)