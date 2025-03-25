from rest_framework import serializers
from ..models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class LlmRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True, 
        max_length=500,  # Set max length to avoid very long input
        error_messages={"required": "Question parameter is required."}
    )
    temperature = serializers.FloatField(
        default=0.7, 
        min_value=0, 
        max_value=1,  # Ensures temperature is between 0 and 1
        error_messages={
            "invalid": "Temperature must be a number.",
            "min_value": "Temperature must be at least 0.",
            "max_value": "Temperature must not exceed 1."
        }
    )
    llm = serializers.ChoiceField(
        default='llama',
        choices=['llama', 'deepseek', 'gemma'],

    )
    convert_to_language = serializers.CharField(
        default='urdu',
        required=False,
        max_length=500
    )