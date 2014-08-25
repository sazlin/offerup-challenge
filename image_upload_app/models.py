from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from image_upload_app.tasks import checkForDuplicates

#sourced w/ modifiation from http://djangotricks.blogspot.com/2013/12/how-to-store-your-media-files-in-amazon.html
def upload_image_to(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'images/%s%s' % (
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class Image(models.Model):
    fileName = models.ImageField(upload_to=upload_image_to)
    Duplicate = models.NullBooleanField()
    Hash = models.CharField(max_length=72, blank=True)


@receiver(signal=post_save, sender=Image)
def image_post_save(sender, instance, created, *args, **kwargs):
    if created:
        print 'image created --> checking for dupes'
        checkForDuplicates.delay(instance.id)
#dispatcher.connect(image_post_save, signal=signals.post_save, sender=Image)
