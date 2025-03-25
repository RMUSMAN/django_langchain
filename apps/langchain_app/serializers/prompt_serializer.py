from rest_framework import serializers

class LLMRequestSerializer(serializers.Serializer):
    sentence = serializers.CharField(
        required=True, 
        max_length=500,  # Set max length to avoid very long input
        error_messages={"required": "Sentence parameter is required."}
    )
    convert_to_language = serializers.CharField(
        default='urdu',
        required=False,
        max_length=500
    )
    llm = serializers.ChoiceField(
        default='llama',
        choices=['llama', 'deepseek', 'gemma'],

    )
    role = serializers.CharField(
        default='chatbot',
        required=False,
        max_length=500
    )