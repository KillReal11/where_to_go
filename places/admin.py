from django.contrib import admin
from places.models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Image)
