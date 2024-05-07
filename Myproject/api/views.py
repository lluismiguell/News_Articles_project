from rest_framework.response import Response
from rest_framework.decorators import api_view
from News_Articles.models import News_Article, Author, Category
from .serializers import News_Article_Serializer, Authors_Serializer, Categories_Serializer

# Create your views here.
@api_view(['GET'])
def getData(request):
    items = News_Article.objects.all()
    serializer = News_Article_Serializer(items, many =True)
    return Response(serializer.data)

@api_view(['GET'])
def getAuthors(request):
    items = Author.objects.all()
    serializer = Authors_Serializer(items, many =True)
    return Response(serializer.data)

@api_view(['GET'])
def getCats(request):
    items = Category.objects.all()
    serializer = Categories_Serializer(items, many =True)
    return Response(serializer.data)

