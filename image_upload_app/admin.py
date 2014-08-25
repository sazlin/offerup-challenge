from django.contrib import admin
from image_upload_app.models import Image


class ImageAdmin(admin.ModelAdmin):
    def image_link(self, image):
        return u"<a href='{}'>{}</a>".format(image.fileName.url, image.fileName)
    image_link.allow_tags = True

    fields = ('id', 'fileName', 'Duplicate', 'Hash')
    list_display = ('id', 'image_link', 'Duplicate', 'Hash')
    readonly_fields = ('id', 'fileName', 'Duplicate', 'Hash')

admin.site.register(Image, ImageAdmin)
