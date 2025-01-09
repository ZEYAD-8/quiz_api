from rest_framework import serializers
from .models import Question, MCQ, MatchingPair, OrderingItem
from categories.models import Category
from quizzes.models import Quiz


class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['text', 'is_correct']


class MatchingPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingPair
        fields = ['item', 'match']


class OrderingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderingItem
        fields = ['text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = MCQSerializer(many=True, required=False)
    matching_pairs = MatchingPairSerializer(many=True, required=False)
    ordering_items = OrderingItemSerializer(many=True, required=False)
    quizzes = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Quiz.objects.all(), write_only=True)
    category = serializers.SerializerMethodField()
    difficulty = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'question_type', 'choices', 'matching_pairs', 'ordering_items', 
            'tf_correct_answer', 'category', 'explanation', 'difficulty', 'quizzes'
        ]

    def get_category(self, obj):
        if obj.category:
            return {"id": obj.category.id, "name": obj.category.name, "slug": obj.category.slug}
        return None

    def get_difficulty(self, obj):
        return obj.get_difficulty_display()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
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

        difficulty = self.initial_data.get('difficulty')
        if difficulty:
            difficulty_map = {string: number for number, string in Question.DIFFICULTY_CHOICES}

            if isinstance(difficulty, str) and difficulty in difficulty_map.keys():
                data['difficulty'] = difficulty_map[difficulty]
            elif isinstance(difficulty, int) and difficulty in difficulty_map.values():
                data['difficulty'] = difficulty
            else:
                raise serializers.ValidationError(
                        {"difficulty": f"Invalid difficulty '{difficulty}'. Should be an integer or a string.",
                        "Valid options": difficulty_map}
                )

        return data

    def validate(self, data):
        category = data.get('category')
        if not category:
            raise serializers.ValidationError("Category is required.")

        question_type = data.get('question_type')
        choices = data.get('choices', [])
        matching_pairs = data.get('matching_pairs', [])
        ordering_items = data.get('ordering_items', [])

        if not question_type:
            raise serializers.ValidationError("Question type is required.")
        elif question_type not in [Question.MULTIPLE_CHOICE, Question.MATCHING, Question.ORDERING, Question.TRUE_FALSE]:
            raise serializers.ValidationError("Invalid question type.")

        if question_type == Question.MULTIPLE_CHOICE and not choices:
            raise serializers.ValidationError("At least one choice is required for multiple-choice questions.")
        elif question_type == Question.MATCHING and not matching_pairs:
            raise serializers.ValidationError("At least one pair is required for matching questions.")
        elif question_type == Question.ORDERING and not ordering_items:
            raise serializers.ValidationError("At least one item is required for ordering questions.")
        elif question_type == Question.TRUE_FALSE and data.get('tf_correct_answer', None) is None:
            raise serializers.ValidationError("True/False questions require a correct answer.")

        return data

    def create(self, validated_data):
        question_type = validated_data.get('question_type')
        choices_data = validated_data.pop('choices', [])
        matching_pairs_data = validated_data.pop('matching_pairs', [])
        ordering_items_data = validated_data.pop('ordering_items', [])
        quizzes = validated_data.pop('quizzes', [])

        user = self.context['request'].user
        validated_data['user'] = user
        question = Question.objects.create(**validated_data)

        if question_type == Question.MULTIPLE_CHOICE:
            for choice_data in choices_data:
                try:
                    choice_data['question'] = question
                    MCQ.objects.create(**choice_data)
                except Exception as e:
                    question.delete()
                    raise serializers.ValidationError("Invalid choice data.")

        elif question_type == Question.MATCHING:
            for pair_data in matching_pairs_data:
                try:
                    pair_data['question'] = question
                    MatchingPair.objects.create(**pair_data)
                except Exception as e:
                    question.delete()
                    raise serializers.ValidationError("Invalid matching pair data.")

        elif question_type == Question.ORDERING:
            for item_data in ordering_items_data:
                try:
                    item_data['question'] = question
                    OrderingItem.objects.create(**item_data)
                except Exception as e:
                    question.delete()
                    raise serializers.ValidationError("Invalid ordering item data.")

        if quizzes:
            question.quizzes.set(quizzes)

        if not question.validate_choices():
            question.delete()
            raise serializers.ValidationError("Invalid choices for multiple-choice question.")

        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.tf_correct_answer = validated_data.get('tf_correct_answer', instance.tf_correct_answer)
        instance.category = validated_data.get('category', instance.category)
        instance.explanation = validated_data.get('explanation', instance.explanation)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)

        quizzes = validated_data.pop('quizzes', None)
        if quizzes is not None:
            instance.quizzes.set(quizzes)

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
