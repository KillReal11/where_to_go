from django.contrib import admin
from where_to_go.models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline, SortableAdminBase


class ImageInline(SortableTabularInline):
    model = Image
    extra = 1
    readonly_fields = ['preview']
    fields = ['file', 'preview', 'position_number']

    def preview(self, image):
        return format_html(
            '<img src="{url}" style="max-height: 200px; max-width: 200px; margin: 5px;"/>',
            url=image.file.url,
        )


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['preview']
    raw_id_fields = ['place']

    def preview(self, Image):
        return format_html(
            '<img src="{url}" style="max-height: 200px; max-width: 200px; margin: 5px;"/>',
            url=Image.file.url,
        )
