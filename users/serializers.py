from rest_framework import serializers
from .models import UserCustom
from django.contrib.auth.password_validation import validate_password
from quizzes.serializers import QuizSerializer, QuestionSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    is_creator = serializers.BooleanField(default=False)

    class Meta:
        model = UserCustom
        fields = ['email', 'password', 'password_confirm', 'is_creator']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['username'] = "Username is not used"
        validated_data['is_admin'] = False
        user = UserCustom.objects.create_user(**validated_data)
        return user


class UserCustomSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    id = serializers.IntegerField(read_only=True)
    number_of_created_quizzes = serializers.SerializerMethodField(read_only=True)
    number_of_created_questions = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserCustom
        fields = ['id', 'email', 'is_creator', 'password', 'number_of_created_quizzes', 'number_of_created_questions']


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserCustom.objects.create_user(password=password, **validated_data)
        return user

    def get_number_of_created_quizzes(self, obj):
        return obj.created_quizzes().count()
    
    def get_number_of_created_questions(self, obj):
        return obj.created_questions().count()
