from rest_framework import serializers
from .models import Category
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    number_of_questions = serializers.SerializerMethodField()
    number_of_quizzes = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'number_of_questions', 'number_of_quizzes']

    def get_number_of_questions(self, obj):
        return obj.questions.count()

    def get_number_of_quizzes(self, obj):
        return obj.quizzes.count()
    
    def create(self, validated_data):
        name = validated_data['name']
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": "Category with this name already exists"})
        
        if 'slug' not in validated_data:
            slug = slugify(name)
            duplicates = Category.objects.filter(slug__iexact=slug)
            if duplicates.exists():
                slug = f"{slug}-{duplicates.count() + 1}"
            
            validated_data['slug'] = slug

        return Category.objects.create(**validated_data)
