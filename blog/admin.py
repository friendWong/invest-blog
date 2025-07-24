from django.contrib import admin
from .models import Category, Post, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_on')
    list_filter = ('category', 'author', 'created_on')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment)
admin.site.register(Like)