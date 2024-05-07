from django.db import models

# Create your models here.

class News_Article(models.Model):

    title = models.CharField(max_length=500)
    summary = models.TextField()
    content = models.TextField()
    published = models.CharField(max_length=500)
    pub_date = models.DateField()
    category = models.CharField(max_length=500)
    author = models.TextField()

    def __str__(self):
        return self.title
    
class Category(models.Model):

    category = models.TextField()

    def __str__(self):
        return self.category
    
class Author(models.Model):

    Uni_author = models.TextField()

    def __str__(self):
        return self.Uni_author

