# makeVoice/serializers.py
from rest_framework import serializers
from makeVoice.models import VoiceList
from customer_ai.models import LLM

# VoiceList Serializer
class VoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceList
        fields = [
            'id',
            'user',
            'llm',
            'sample_url',
            'created_at',
            'voice_name',
            'voice_image',
            'is_public',
            'voice_id',
            'voice_like_count',
            'celebrity',
        ]
        read_only_fields = ['id', 'created_at', 'voice_like_count']

# LLM Serializer
class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM
        fields = [
            'id',
            'user',
            'voice',
            'genres',
            'name',
            'prompt',
            'created_at',
            'update_at',
            'llm_image',
            'response_mp3',
            'model',
            'language',
            'temperature',
            'stability',
            'speed',
            'style',
            'is_public',
            'title',
            'description',
            'llm_like_count',
            'llm_background_image',
            'invest_count',
        ]
        read_only_fields = ['id', 'created_at', 'update_at', 'llm_like_count']
