from django.contrib import admin
from app.models import Category, Comment, Post, Journal

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_private')
    list_filter = ('author',)
    search_fields = ('title', 'author')

class CommentAdmin(admin.ModelAdmin):
    pass

class JournalAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on')
    search_fields = ('author',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Journal, JournalAdmin)