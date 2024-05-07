from django.shortcuts import render
from .models import News_Article

# Create your views here.
def News_Articles(request):
    Articles = News_Article.objects.all()
    return render(request, 'News_Articles/News_Articles.html', {'Articles' : Articles})
