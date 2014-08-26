from django.test import TestCase
from django.test.utils import override_settings
from django.core.files import File
from image_upload_app.models import Image


class TaskTests(TestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                                CELERY_ALWAYS_EAGER=True)
    def setUp(self):
        Image.objects.create(fileName=File(open("./test_collateral/60.jpg")))
        Image.objects.create(fileName=File(open("./test_collateral/65.jpg")))
        Image.objects.create(fileName=File(open("./test_collateral/60.jpg")))
        self.images = Image.objects.all()
        print self.images[0].id, self.images[0].fileName, self.images[0].Duplicate, self.images[0].Hash
        print self.images[1].id, self.images[1].fileName, self.images[1].Duplicate, self.images[1].Hash
        print self.images[2].id, self.images[2].fileName, self.images[2].Duplicate, self.images[2].Hash
        # print Image.objects.all()[0].id, Image.objects.all()[0].fileName, Image.objects.all()[0].Duplicate, Image.objects.all()[0].Hash

    def tearDown(self):
        print "tearing down..."
        self.images[0].delete()
        self.images[0].delete()
        self.images[0].delete()

    def test_checkForDuplicates_no_dupe(self):
        self.assertIs(self.images[0].Duplicate, False)
        self.assertIs(self.images[1].Duplicate, False)

    def test_checkForDuplicates_dupe(self):
        self.assertTrue(self.images[2].Duplicate)

    def test_checkForDuplicates_doesnt_exist(self):
        """
        Test that checkForDuplicates fails gracefully when the task
        is asked to check for duplicates of an image that doesn't exist.
        """
        from image_upload_app.tasks import checkForDuplicates
        self.assertIsNone(checkForDuplicates(-1))
