from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)
    show_change_link = True

    class Media:
        css = {'all': ('admin/css/drag-drop.css',)}
        js = ('admin/js/drag-drop.js',)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('position')


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 400px; display: block; margin: 10px 0;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title','lat', 'lng', 'images_count')
    list_editable = ('lat', 'lng')
    search_fields = ('title',)
    inlines = [ImageInline]


    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request, obj) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request, obj):
                    inline.max_num = 0
            inline_instances.append(inline)
        return inline_instances


    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Фотографии'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'image_preview')
    list_filter = ('place',)
    

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 80px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'