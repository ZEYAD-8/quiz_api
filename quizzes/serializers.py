from rest_framework import serializers
from .models import Quiz, Question, MCQ, MatchingPair, OrderingItem

# A serializer for each type of question (MCQ, MatchingPair, OrderingItem)
class MCQSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    class Meta:
        model = MCQ
        fields = ['id', 'text', 'is_correct', 'question']


class MatchingPairSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    class Meta:
        model = MatchingPair
        fields = ['id', 'item', 'match', 'question']


class OrderingItemSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    class Meta:
        model = OrderingItem
        fields = ['id', 'text', 'order', 'question']



class QuestionSerializer(serializers.ModelSerializer):
    choices = MCQSerializer(many=True, required=False)
    matching_pairs = MatchingPairSerializer(many=True, required=False)
    ordering_items = OrderingItemSerializer(many=True, required=False)
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'question_type', 'tf_correct_answer', 
            'choices', 'matching_pairs', 'ordering_items'
        ]

    def create(self, validated_data):
        question_type = validated_data.get('question_type')
        choices_data = validated_data.pop('choices', [])
        matching_pairs_data = validated_data.pop('matching_pairs', [])
        ordering_items_data = validated_data.pop('ordering_items', [])

        if question_type == Question.MULTIPLE_CHOICE and not choices_data:
            raise serializers.ValidationError("At least one choice is required for multiple-choice questions.")
        elif question_type == Question.MATCHING and not matching_pairs_data:
            raise serializers.ValidationError("At least one pair is required for matching questions.")
        elif question_type == Question.ORDERING and not ordering_items_data:
            raise serializers.ValidationError("At least one item is required for ordering questions.")

        # validated_data['quiz'] = Quiz.objects.get(id=3)
        question = Question.objects.create(**validated_data)

        if question_type == Question.MULTIPLE_CHOICE:
            for choice_data in choices_data:
                try:
                    choice_data['question'] = question
                    MCQ.objects.create(**choice_data)
                except Exception as e:
                    print(e)
                    question.delete()
                    raise serializers.ValidationError("Invalid choice data.")

        elif question_type == Question.MATCHING:
            for pair_data in matching_pairs_data:
                try:
                    pair_data['question'] = question
                    MatchingPair.objects.create(**pair_data)
                except Exception as e:
                    print(e)
                    question.delete()
                    raise serializers.ValidationError("Invalid matching pair data.")

        elif question_type == Question.ORDERING:
            for item_data in ordering_items_data:
                try:
                    item_data['question'] = question
                    OrderingItem.objects.create(**item_data)
                except Exception as e:
                    print(e)
                    question.delete()
                    raise serializers.ValidationError("Invalid ordering item data.")

        if not question.validate_choices():
            question.delete()
            raise serializers.ValidationError("Invalid choices for multiple-choice question.")

        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.tf_correct_answer = validated_data.get('tf_correct_answer', instance.tf_correct_answer)
        instance.save()

        if instance.question_type == Question.MULTIPLE_CHOICE:
            choices_data = validated_data.get('choices')
            if choices_data is not None:
                self.update_nested(instance, 'choices', MCQ, choices_data)

        if instance.question_type == Question.MATCHING:
            matching_pairs_data = validated_data.get('matching_pairs')
            if matching_pairs_data is not None:
                self.update_nested(instance, 'matching_pairs', MatchingPair, matching_pairs_data)

        if instance.question_type == Question.ORDERING:
            ordering_items_data = validated_data.get('ordering_items')
            if ordering_items_data is not None:
                self.update_nested(instance, 'ordering_items', OrderingItem, ordering_items_data)

        return instance

    def update_nested(self, question, related_name, model_class, data):
        field_name = getattr(question, related_name)

        existing_items = {}
        for item in field_name.all():
            existing_items[item.id] = item

        for item_data in data:
            item_data['question'] = question
            model_class.objects.create(**item_data)

        for item_id in existing_items.keys():
            existing_items[item_id].delete()


# A quiz serializer that includes the questions
class QuizSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'questions']


    def validate(self, data):
        # Ensure there are questions
        questions_data = data.get('questions', [])
        if not questions_data:
            raise serializers.ValidationError("At least one question is required.")

        # Validate each question but don't save yet
        for question_data in questions_data:
            question_serializer = QuestionSerializer(data=question_data)
            if not question_serializer.is_valid():
                raise serializers.ValidationError(f"Invalid question data: {question_serializer.errors}")

        return data


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
    
        # Extract questions data from the input
        questions_data = validated_data.pop('questions', [])
        
        # Create the quiz instance
        quiz = Quiz.objects.create(**validated_data)
        
        for question_data in questions_data:
            question_data['quiz'] = quiz
            QuestionSerializer().create(validated_data=question_data)
        
        return quiz
