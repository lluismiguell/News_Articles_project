from django.contrib import admin
from .models import News_Article, Author, Category

# Register your models here.
admin.site.register(News_Article)
admin.site.register(Author)
admin.site.register(Category)