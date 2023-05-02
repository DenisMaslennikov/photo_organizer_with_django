from django.contrib import admin

from image.models import Image
from tag_anything.models import Tag, TagCategory


class TagAdmin(admin.ModelAdmin):

    list_display = (
        'tag',
        'category',
    )
    list_editable = (
        'category',
    )


admin.site.register(Image)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagCategory)
