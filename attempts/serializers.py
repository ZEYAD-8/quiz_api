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


class QuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = ['question', 'answer']


class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = QuestionAttemptSerializer(many=True, write_only=True)
    attempt = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = QuizAttempt
        fields = ['answers',
                'attempt', 'user', 'quiz', 'total_questions', 'total_questions_answered', 'total_correct', 'user_score', 'max_score']
        read_only_fields = ['attempt', 'user', 'quiz', 'total_questions', 'total_questions_answered', 'total_correct', 'user_score', 'max_score']

    def get_attempt(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.user.id

    def create(self, validated_data):
        question_attempts_data = validated_data.pop('answers')
        quiz = validated_data['quiz']
        quiz_attempt = QuizAttempt.objects.create(**validated_data)
        
        total_score = 0
        quiz_attempt.total_questions = quiz.questions.count()
        quiz_attempt.total_questions_answered = len(question_attempts_data)


        for question_attempt_data in question_attempts_data:
            question = question_attempt_data['question']
            user_answer = question_attempt_data['answer']

            is_correct = True
            QuestionAttempt.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                answer=user_answer,
                is_correct=is_correct
            )
            if is_correct:
                total_score += 1

        quiz_attempt.user_score = total_score
        quiz_attempt.total_correct = total_score
        quiz_attempt.max_score = quiz_attempt.total_questions
        quiz_attempt.save()
        return quiz_attempt
