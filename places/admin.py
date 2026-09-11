from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['preview']
    fields = ["file", "preview", "position_number"]

    def preview(self, place):
        return format_html(
            '<img src="{url}" style="max-height: 100px; margin: 5px;"/>',
            url=place.file.url,
        )



@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Image)
