from rest_framework import serializers
from .models import Quiz
from categories.models import Category
from questions.models import Question
from questions.serializers import QuestionSerializer

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()
    number_of_questions = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'number_of_questions', 'questions']


    def validate(self, data):
        questions_data = data.get('questions', [])
        if not questions_data:
            raise serializers.ValidationError("At least one question is required.")

        return data

    def get_category(self, obj):
        if obj.category:
            return {"id": obj.category.id, "name": obj.category.name, "slug": obj.category.slug}
        return None

    def get_number_of_questions(self, obj):
        return obj.questions.count()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        # questions will be an array of question IDs
        questions = self.initial_data.get('questions', [])
        data['questions'] = []
        for question_id in questions:
            try:
                question = Question.objects.get(id=question_id)
                data['questions'].append(question)
            except Question.DoesNotExist:
                raise serializers.ValidationError({"questions": f"Question with ID {question_id} does not exist."})

        category = self.initial_data.get("category")
        if category:
            if isinstance(category, int):
                try:
                    data['category'] = Category.objects.get(id=category)
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category": "Invalid category ID."})
            elif isinstance(category, str):
                try:
                    data['category'] = Category.objects.get(slug__iexact=category)
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category": "Invalid category slug."})
            else:
                raise serializers.ValidationError({"category": "Invalid category identifier. Should be an integer or a string."})

        return data



    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        questions = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(**validated_data)
        quiz.questions.set(questions)
        return quiz


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()

        questions = validated_data.pop('questions', [])
        instance.questions.set(questions)
        return instance
