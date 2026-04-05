from django.contrib import admin

from blog.models import Article, Image


class ImageInline(admin.StackedInline):
    model = Image


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'author')
    list_filter = ('author', 'date_posted')
    fields = [('title', 'author', 'content')]
    inlines = [
        ImageInline,
    ]


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    list_filter = ('id_title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Image, ImageAdmin)
