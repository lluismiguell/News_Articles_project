from rest_framework import serializers
from News_Articles.models import News_Article, Category, Author

class News_Article_Serializer(serializers.ModelSerializer):
    class Meta:
        model = News_Article
        fields = '__all__'

class Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class Authors_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'