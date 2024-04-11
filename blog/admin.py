from django.contrib import admin
from .models import Post, Comment,  Category, RepliedComment


admin.site.site_header = "Entire and Fit"
admin.site.site_title = " Entire and Fit"
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_posts', 'category_slug')
    prepopulated_fields = {'category_slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'publish', )
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def category(self, obj):
        return obj.category


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', )
    prepopulated_fields = {'comment_slug': ('comment_body',)}


@admin.register(RepliedComment)
class RepliedCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active', 'comment')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email',)


