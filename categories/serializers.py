from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    number_of_questions = serializers.SerializerMethodField()
    number_of_quizzes = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'number_of_questions', 'number_of_quizzes']

    def get_number_of_questions(self, obj):
        return obj.questions.count()

    def get_number_of_quizzes(self, obj):
        return obj.quizzes.count()
