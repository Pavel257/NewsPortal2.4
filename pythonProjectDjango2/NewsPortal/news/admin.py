from django.contrib import admin
from .models import *


class PostCategoryInLine(admin.StackedInline):
    model = PostCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'id', 'title', 'dateCreation',)
    list_filter = ('author', 'dateCreation',)
    list_display_links = ('author',)
    inlines = [PostCategoryInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ("name",)
    inlines = [PostCategoryInLine]


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough',)


# @admin.register(Author)
# class Author(admin.ModelAdmin)

admin.site.register(Author)
admin.site.register(Comment)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(PostCategory)
