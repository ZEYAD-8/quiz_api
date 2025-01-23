from rest_framework import serializers
from .models import QuizAttempt, QuestionAttempt
from questions.models import Question

class QuestionReadAttemptSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    difficulty = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'details', 'category', 'difficulty']

    def get_category(self, obj):
        if obj.category:
            return {"id": obj.category.id, "name": obj.category.name, "slug": obj.category.slug}
        return None

    def get_difficulty(self, obj):
        return obj.get_difficulty_display()


    def get_details(self, obj):
        if obj.question_type == Question.MULTIPLE_CHOICE:
            choices = obj.choices.all().values_list('text', flat=True)
            return choices

        elif obj.question_type == Question.MATCHING:
            items = [pair.item for pair in obj.matching_pairs.all()]
            matches = [pair.match for pair in obj.matching_pairs.all()]
            return {
                "items": items,
                "matches": matches
            }

        elif obj.question_type == Question.ORDERING:
            items = obj.ordering_items.all().values_list('text', flat=True)
            return items

        elif obj.question_type == Question.TRUE_FALSE:
            return 'True/False'

        return None



class QuizReadAttemptSerializer(serializers.ModelSerializer):
    questions = QuestionReadAttemptSerializer(many=True)
    class Meta:
        model = QuizAttempt
        fields = ['id', 'questions']


