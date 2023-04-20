from .models import Settings, Tag, Image
import os

batch_size = 10000


def scan_dirs():
    extensions = Settings.objects.filter(setting_name='img_extensions')
    extensions = [val.setting_value for val in extensions]
    for dir in Settings.objects.filter(setting_name='scan_dirs'):
        bulk_img = []
        tags = []
        if os.path.isdir(dir.setting_value):
            for path, dirs, files in os.walk(dir.setting_value):
                for file in files:
                    if (os.path.splitext(file)[-1] in extensions):

                        if os.path.split(path)[-1] not in tags:
                            tags.append(os.path.split(path)[-1])
                            Tag.objects.update_or_create(
                                tag=os.path.split(path)[-1])

                        bulk_img.append(Image(
                            image_path=os.path.abspath(
                                os.path.join(path, file)),
                            image_name=os.path.splitext(file)[0],
                            ))

        Image.objects.bulk_create(bulk_img,
                                  batch_size=batch_size,
                                  ignore_conflicts=True)

    _bulk_image_tags()


def _bulk_image_tags():
    for tag in Tag.objects.all():
        tag.image_set.add(*Image.objects.filter(image_path__contains=os.sep
                                                + tag.tag + os.sep))
