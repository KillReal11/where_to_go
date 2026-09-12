from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline, SortableAdminMixin


class ImageInline(SortableTabularInline):
    model = Image
    extra = 1
    readonly_fields = ['preview']
    fields = ["file", "preview", "position_number"]

    def preview(self, image):
        return format_html(
            '<img src="{url}" style="max-height: 200px; margin: 5px;"/>',
            url=image.file.url,
        )


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['preview']

    def preview(self, Image):
        return format_html(
            '<img src="{url}" style="max-height: 200px; margin: 5px;"/>',
            url=Image.file.url,
        )
