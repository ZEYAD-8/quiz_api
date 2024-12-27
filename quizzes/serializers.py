from rest_framework import serializers
from .models import Quiz, Question, MCQ, MatchingPair, OrderingItem


class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['id', 'text', 'is_correct']


class MatchingPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingPair
        fields = ['id', 'item', 'match']


class OrderingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderingItem
        fields = ['id', 'text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'answers']

    def get_answers(self, obj):
        if obj.question_type == Question.MULTIPLE_CHOICE:
            return MCQSerializer(obj.mcqs.all(), many=True).data
        elif obj.question_type == Question.MATCHING:
            return MatchingPairSerializer(obj.matching_pairs.all(), many=True).data
        elif obj.question_type == Question.ORDERING:
            return OrderingItemSerializer(obj.ordering_items.all(), many=True).data
        elif obj.question_type == Question.TRUE_FALSE:
            return {"answer": obj.tf_correct_answer}
        return None

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)  # Nested serializer for questions

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'questions']
